#!/usr/bin/env python3
"""视频渲染基准测试：复现《万人灯》weave.py 的管线结构（PIL 静帧 + ffmpeg zoompan + x264）。

工作负载：10 个分段 x 6 秒 = 60 秒，720p（1280x720），30fps，纯视频（无音频/TTS/音乐）。
每段 = 1 张 PIL 静帧（渐变底 + 光晕高斯模糊 + 贴图 + 中文注文）
       + ffmpeg zoompan 缓推 + 淡入淡出，libx264 preset medium crf 20。

用法：
  全量（云电脑基线 / 单台 InstaBox）：python3 bench.py --start 0 --count 10 --out out
  分段（5 台并行，每台 2 段）：          python3 bench.py --start 0 --count 2 --out out
                                     python3 bench.py --start 2 --count 2 --out out
                                     ...（start=0/2/4/6/8）
  拼接（收齐 10 段后）：                 python3 bench.py --concat out --out out

输出：每阶段耗时 JSON（stdout 最后一行），便于跨机器对比。
注意：不复现《洛神赋》的 HTML canvas 逐帧抓取路径（需 headless Chromium，
逐帧成本更高）；本测试只覆盖 PIL 静帧 + ffmpeg 编码这一类工作负载。
"""
import argparse
import json
import os
import random
import subprocess
import sys
import time

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1280, 720
FPS = 30
SEG_DUR = 6.0

TEXTS = [
    "一盏灯，一句话", "长夜里有人点灯", "灯火沿街次第亮起",
    "字是写在光里的", "风过处，灯影摇", "一盏接一盏",
    "夜被灯火缝住", "远远望去像一条河", "灯下有人低语",
    "天亮之前，灯不灭",
]


def find_font(bold=False):
    cands = [
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc" if bold
        else "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSerifCJK-Regular.ttc",
        "/usr/share/fonts/noto-cjk/NotoSerifCJK-Regular.ttc",
    ]
    for c in cands:
        if os.path.exists(c):
            return c
    return None


def base_image(seed):
    """程序化生成一张细节丰富的底图（渐变 + 随机圆 + 噪点），供编码器吃满负荷。"""
    rng = random.Random(seed)
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    top, bot = (16, 19, 46), (4, 5, 13)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)],
               fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    for _ in range(40):
        x, y = rng.randint(0, W), rng.randint(0, H)
        r = rng.randint(20, 120)
        col = (rng.randint(80, 255), rng.randint(60, 200), rng.randint(40, 120))
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    noise = Image.effect_noise((W, H), 28).convert("RGB")
    return Image.blend(img, noise, 0.25)


def render_still(i, out_path):
    """照 weave.py 的路子画一张静帧：渐变底 + 光晕 + 贴图 + 注文。"""
    img = base_image(1000 + i)
    # 光晕：与 weave.py 的 add_glow 同构（mask + GaussianBlur）
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    for r in range(300, 0, -8):
        a = int(110 * (1 - r / 300) ** 1.6)
        md.ellipse([W // 2 - r, 240 - r, W // 2 + r, 240 + r], fill=a)
    mask = mask.filter(ImageFilter.GaussianBlur(40))
    glow = Image.new("RGB", (W, H), (255, 172, 92))
    img = Image.composite(glow, img, mask)
    # 注文
    d = ImageDraw.Draw(img)
    font_path = find_font(bold=False)
    font_b = find_font(bold=True)
    if font_path:
        f_big = ImageFont.truetype(font_b or font_path, 64)
        f_small = ImageFont.truetype(font_path, 30)
    else:
        f_big = ImageFont.load_default()
        f_small = ImageFont.load_default()
    text = TEXTS[i % len(TEXTS)]
    d.text((W // 2, H // 2 - 30), text, font=f_big, fill=(245, 240, 230),
           anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
    d.text((W // 2, H - 60), f"第 {i + 1:02d} 段 / 共 10 段", font=f_small,
           fill=(201, 168, 106), anchor="mm")
    img.save(out_path)
    return out_path


def build_segment(i, pic, out_path):
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"zoompan=z='min(1+0.0009*on,1.14)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},"
          f"fade=t=in:st=0:d=0.7,fade=t=out:st={SEG_DUR - 0.7:.2f}:d=0.7")
    cmd = ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS),
           "-i", pic, "-filter_complex", f"[0:v]{vf}[v]",
           "-map", "[v]", "-t", f"{SEG_DUR:.2f}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-r", str(FPS), out_path]
    subprocess.run(cmd, check=True)
    return out_path


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration", "-show_entries",
                          "stream=width,height,codec_name",
                          "-of", "json", path],
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--count", type=int, default=10)
    ap.add_argument("--out", required=True)
    ap.add_argument("--concat", action="store_true",
                    help="只拼接：把 out/segNN.mp4（须齐 10 段）拼成 60 秒成片")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    t0 = time.perf_counter()
    stages = {}

    if args.concat:
        lst = os.path.join(args.out, "list.txt")
        with open(lst, "w") as f:
            for i in range(10):
                p = os.path.join(args.out, f"seg{i:02d}.mp4")
                assert os.path.exists(p), f"missing segment {p}"
                f.write(f"file '{os.path.abspath(p)}'\n")
        t = time.perf_counter()
        final = os.path.join(args.out, "film_60s.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                        "-i", lst, "-c", "copy", final], check=True)
        stages["concat_s"] = round(time.perf_counter() - t, 2)
        info = probe(final)
        stages["film"] = info
        stages["total_s"] = round(time.perf_counter() - t0, 2)
        print(json.dumps(stages, ensure_ascii=False))
        return

    t = time.perf_counter()
    pics = []
    for i in range(args.start, args.start + args.count):
        pics.append(render_still(i, os.path.join(args.out, f"still{i:02d}.png")))
    stages["pil_stills_s"] = round(time.perf_counter() - t, 2)

    t = time.perf_counter()
    segs = []
    for k, i in enumerate(range(args.start, args.start + args.count)):
        segs.append(build_segment(i, pics[k], os.path.join(args.out, f"seg{i:02d}.mp4")))
    stages["ffmpeg_segments_s"] = round(time.perf_counter() - t, 2)
    stages["segments"] = [os.path.basename(s) for s in segs]
    stages["total_s"] = round(time.perf_counter() - t0, 2)
    print(json.dumps(stages, ensure_ascii=False))


if __name__ == "__main__":
    main()
