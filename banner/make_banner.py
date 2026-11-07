# -*- coding: utf-8 -*-
"""
复刻 yetone 主页 banner：CRT 绿磷光终端 GIF
===============================================
核心: x0rzavi/github-readme-terminal (pip 包名 github-readme-terminal, 模块 gifos, MIT)
      + Pillow 后期处理 (CRT 显示器边框 / 扫描线 / 磷光辉光 / 开机动画 / 故障条纹)
      + ffmpeg (由 imageio-ffmpeg 提供, palettegen 压缩)

用法:
    python make_banner.py                # 用下方 CONFIG 与本地头像生成
    python make_banner.py --user xxx     # 从 GitHub 拉取 xxx 的头像

依赖:
    pip install github-readme-terminal imageio-ffmpeg pillow
"""

import argparse
import os
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

# ---------------------------------------------------------------------------
# 配置（改成你自己的）
# ---------------------------------------------------------------------------
CONFIG = {
    "user": "eugenewang5425",
    "display_name": "eugene",
    "shell_user": "eugenewang5425",
    "host": "mbp",  # 提示符样式: shell_user@host$
    "cmd": "fetch.sh",  # 顶部输入的命令
    "info": [
        # (标签, 值) —— 右侧 neofetch 式信息
        ("Name",     "eugene"),
        ("Age",      "23"),
        ("Work",     "Student · Robotics"),
        ("OS",       "Windows 11"),
        ("Editor",   "VS Code"),
        ("Languages", "Python, TypeScript, C++"),
        ("Skills",   "GIS, RS, Robotics"),
    ],
    "txt_color": "#5cf066",  # 单一的纯绿色
    "bg_color":  "#0c1f10",
}

# 屏幕逻辑分辨率（gifos 用 gohufont 位图字体 14px）
# 终端原生渲染 720x450 = 内容尺寸, 屏幕 800x500, 全程零缩放 -> 字形 1:1 无损伤
TERM_W, TERM_H = 720, 450
W, H = 800, 500
FPS = 15
FONT_SIZE = 14
AVATAR_GRID = 56        # 头像像素化后的网格边长
AVATAR_PIXEL = 5        # 每个"像素块"的边长 (终端坐标)
FONT_WIDTH = 8          # gohufont 位图字符宽

WORK = Path(__file__).parent / "_build"
FRAMES_IN = WORK / "frames"        # gifos 默认输出目录(相对 cwd)
FRAMES_OUT = WORK / "crt_frames"
THEME_BG = (13, 17, 23)            # 机壳外填充色(由 --theme 覆盖)


# ---------------------------------------------------------------------------
# 1) 头像 -> 绿色磷光双色调像素画
# ---------------------------------------------------------------------------
def pixelate_avatar(src: Path, dst: Path) -> None:
    img = Image.open(src).convert("RGB")
    side = min(img.size)
    img = img.crop(((img.width - side) // 2, (img.height - side) // 2,
                    (img.width + side) // 2, (img.height + side) // 2))
    small = img.resize((AVATAR_GRID, AVATAR_GRID), Image.NEAREST).convert("L")
    small = ImageOps.autocontrast(small, cutoff=1)

    # 原版风格：亮磷光底 + 暗色网点雕刻 + 白色高光
    # 亮度越高 -> 越接近白; 暗部用深绿填充; 2x2 Bayer 抖动出"网点"质感
    dither = [[0, 3], [3, 1]]
    shades = [(20, 44, 28), (36, 78, 46), (54, 112, 64), (74, 148, 84),
              (96, 184, 104), (122, 220, 128), (156, 250, 158)]
    grid = Image.new("RGB", (AVATAR_GRID, AVATAR_GRID))
    px = grid.load()
    for y in range(AVATAR_GRID):
        for x in range(AVATAR_GRID):
            v = small.getpixel((x, y)) + (dither[x % 2][y % 2] - 1.5) * 16
            if v < 36:
                c = shades[0]
            elif v < 64:
                c = shades[1] if v < 50 else shades[2]
            elif v < 96:
                c = shades[2] if v < 78 else shades[3]
            elif v < 132:
                c = shades[3] if v < 112 else shades[4]
            else:
                c = shades[4] if v < 160 else shades[5]
            px[x, y] = c
    # 亮部随机白色高光点 + 少量深色网点（磷光闪烁质感）
    import random
    out = grid.copy()
    op = out.load()
    for y in range(AVATAR_GRID):
        for x in range(AVATAR_GRID):
            lum = sum(op[x, y]) / 3
            if lum > 110 and random.random() < 0.15:
                op[x, y] = (195, 250, 200)
            elif lum < 90 and random.random() < 0.05:
                op[x, y] = (10, 24, 14)
    big = out.resize((AVATAR_GRID * AVATAR_PIXEL, AVATAR_GRID * AVATAR_PIXEL), Image.NEAREST)
    big.save(dst)


# ---------------------------------------------------------------------------
# 2) 纯绿"息屏进度条"(替代原版右下角的彩色调色板)
# ---------------------------------------------------------------------------
MODULE_START = 113
SHUT_FONT = None


def _region_glow(img, box, blur=6, strength=0.85):
    """给模块区域单独做与主画面一致的磷光辉光。"""
    reg = img.crop(box)
    gl = reg.filter(ImageFilter.GaussianBlur(blur))
    gl = ImageEnhance.Brightness(gl).enhance(strength)
    img.paste(ImageChops.screen(reg, gl), box)


def _term_text(img, d, x, y, s, font, sample=False, fg=(92, 240, 102), cw=8, ch=14):
    """终端式字符文本。
    sample=False: 不擦除(每帧从新屏幕绘制, 无残留);
    sample=True : 逐行采样上方 8px 的像素填充(同扫描线相位), 无缝擦除旧字形。"""
    if sample:
        px = img.load()
        w0 = img.width
        for yy in range(y - 1, y + ch + 2):
            sy = max(0, yy - 8)
            c = px[min(x + 4, w0 - 1), sy]
            d.line([(x - 2, yy), (x + cw * len(s) + 2, yy)], fill=c)
    d.text((x, y), s, fill=fg, font=font)


def draw_shutdown_bar(img, t, x=408, y=254, glow=False):
    """右下角息屏进度条(纯字符, 与其它文字同一风格):
        shutting down 51%
        [#########------------]
    进度从内容加载完(MODULE_START)起, 闪烁段末尾涨到 100%。"""
    import gifos as _gifos
    import os as _os

    global SHUT_FONT
    if SHUT_FONT is None:
        SHUT_FONT = ImageFont.load(_os.path.join(
            _os.path.dirname(_gifos.__file__), "fonts", "gohufont-uni-14.pil"))
    d = ImageDraw.Draw(img)
    progress = min(1.0, (t - MODULE_START + 1) / 170.0)
    _term_text(img, d, x, y, f"shutting down {int(progress * 100):3d}%", SHUT_FONT, sample=glow)
    nfill = int(round(progress * 20))
    bar = "[" + "#" * nfill + "-" * (20 - nfill) + "]"
    _term_text(img, d, x, y + 18, bar, SHUT_FONT, sample=glow)
    if glow:
        _region_glow(img, (x - 4, y - 2, x + 186, y + 38))


# ---------------------------------------------------------------------------
# 3) 用 gifos 生成终端动画帧
# ---------------------------------------------------------------------------
def _reset_occupancy(t) -> None:
    """gifos 会把 paste_image 占用的行记进 __col_in_row,
    之后非连续写入会引发 scroll_up 把内容切掉 —— 贴图后重置,
    告诉 gifos 所有行都是空的。"""
    for r in range(1, t.num_rows + 1):
        t._Terminal__col_in_row[r] = 1


def gen_terminal_frames(avatar_px: Path) -> None:
    from gifos import Terminal

    t = Terminal(width=TERM_W, height=TERM_H, xpad=8, ypad=8,
                 font_size=FONT_SIZE, line_spacing=3)
    t.set_txt_color(CONFIG["txt_color"])
    t.set_bg_color(CONFIG["bg_color"])
    t.set_fps(FPS)
    # 给整块屏幕一个绿色磷光底色(位图字体的光标擦除仍用默认黑)
    t._Terminal__frame = Image.new("RGB", (TERM_W, TERM_H), (12, 30, 16))
    t.set_prompt(f"{CONFIG['shell_user']}@{CONFIG['host']}$")
    # 光标闪烁用的是默认色, 同步成同一个绿
    t._Terminal__def_txt_color = CONFIG["txt_color"]
    t._Terminal__def_bg_color = (12, 30, 16)

    # 顶部命令行：逐字打出
    cmd = f"{CONFIG['shell_user']}@{CONFIG['host']} ~ % {CONFIG['cmd']}"
    t.gen_typing_text(cmd, row_num=1, col_num=1, speed=2)

    # 左侧：像素化头像
    t.paste_image(str(avatar_px), row_num=3, col_num=1, size_multiplier=1)
    _reset_occupancy(t)

    # 右侧：neofetch 式信息逐条出现
    t.gen_text(f"{CONFIG['display_name']}@GitHub", row_num=3, col_num=46, count=3)
    t.gen_text("-" * 32, row_num=4, col_num=46, count=3)
    r = 5
    for label, value in CONFIG["info"]:
        t.gen_text(f"{label}: {value}", row_num=r, col_num=46, count=3)
        r += 1

    # 底部提示符：打出
    t.gen_prompt(row_num=22, col_num=1, count=2)

    # 结尾停留(右下角动态平衡条在 CRT 后期阶段叠加)
    t.clone_frame(55)


# ---------------------------------------------------------------------------
# 4) CRT 后期处理
# ---------------------------------------------------------------------------
def barrel_warp(img, kx=0.05, ky=0.022, edge_dark=0.16):
    """老式曲面屏: 玻璃向观察者凸起(边缘采样外翻, 出现往外凸的球面感)。
    双线性采样: 不会像最近邻那样因采样步长不均而吞掉字形像素
    (缺胳膊少腿的根源), 文字与背景同一张图做变换, 曲率完全统一。"""
    import numpy as np

    w, h = img.size
    arr = np.asarray(img, dtype=np.uint8).astype(np.float32)
    xs = np.linspace(-1, 1, w, dtype=np.float32)
    ys = np.linspace(-1, 1, h, dtype=np.float32)
    xx, yy = np.meshgrid(xs, ys)
    f = 1.0 + (kx * xx * xx + ky * yy * yy)
    sx = ((xx * f) + 1.0) * (w - 1) * 0.5
    sy = ((yy * f) + 1.0) * (h - 1) * 0.5
    x0 = np.floor(sx).astype(np.int32)
    y0 = np.floor(sy).astype(np.int32)
    x0 = np.clip(x0, 0, w - 2)
    y0 = np.clip(y0, 0, h - 2)
    wx = (sx - x0)[:, :, None]
    wy = (sy - y0)[:, :, None]
    p00 = arr[y0, x0]
    p01 = arr[y0, x0 + 1]
    p10 = arr[y0 + 1, x0]
    p11 = arr[y0 + 1, x0 + 1]
    out = (p00 * (1 - wx) * (1 - wy) + p01 * wx * (1 - wy)
           + p10 * (1 - wx) * wy + p11 * wx * wy)
    # 曲面的轻微边缘压暗(仅四角方向)
    dark = 1.0 - edge_dark * (xx * xx + yy * yy) * 0.5
    out = out * dark[:, :, None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def crt_post_process(frames_in: Path, frames_out: Path) -> None:
    import re as _re
    frames_out.mkdir(parents=True, exist_ok=True)
    # gifos 帧名是 frame_1/frame_10/...，必须按数字排序, 否则字符串排序会把动画顺序打乱
    files = sorted(
        frames_in.glob("*.png"),
        key=lambda p: int(_re.search(r"(\d+)", p.name).group(1)),
    )

    # ---- 老式 CRT 外壳: 机壳 + 曲面屏幕开口的深灰面板 ----
    # 屏幕画在机壳/面板"下面", 面板环最后盖上去; 开口与内容同一 barrel 曲率
    import numpy as _np
    MARGIN = 24                         # 机壳与画布边缘的透明边距(不填黑)
    HOLE_RIM = 3                        # 面板环只遮屏幕外圈 3px
    RIMW = 14                           # 内缘(面板环)宽度
    bezel_pad = MARGIN + 32 + RIMW + HOLE_RIM   # 屏幕距画布边 = 24+32+14+3
    CASE_IN = bezel_pad + HOLE_RIM - RIMW       # 机壳内圈 = 面板环外缘
    TR_KEY = THEME_BG                    # 机壳外填充 = 主题页面底色(亮/暗各一张)
    CBW, CBH = W + bezel_pad * 2, H + bezel_pad * 2
    gy = _np.linspace(0, 1, CBH, dtype=_np.float32)[:, None]
    g = _np.broadcast_to(gy, (CBH, CBW))
    # 归一化网格(供光照计算, 提前定义)
    xxm, yym = _np.meshgrid(_np.linspace(0, 1, CBW, dtype=_np.float32),
                            _np.linspace(0, 1, CBH, dtype=_np.float32))
    # === 前脸 = 一整块塑料面板(不再分"机壳/面板"两层, 结构上无接缝) ===
    # 单一光源: 左上环境光 -> 右下渐暗(仅一层光影)
    front_arr = _np.zeros((CBH, CBW, 3), dtype=_np.float32)
    front_arr[:] = _np.array([38, 41, 44], dtype=_np.float32)     # 环境漫散射底
    diag = 1.0 - (xxm + yym) * 0.5                                # 左上 1 -> 右下 0
    front_arr += (diag[:, :, None] * _np.array([42, 43, 45], dtype=_np.float32))
    front_arr *= (0.94 + 0.06 * yym)[:, :, None]                  # 底部略暗
    front = Image.fromarray(_np.clip(front_arr, 30, 255).astype(_np.uint8))
    # 质感: 污渍 / 划痕 / 边缘磨损 / 颗粒
    rng = _np.random.default_rng(42)
    stain = Image.new("RGB", (CBW, CBH), (255, 255, 255))
    sd = ImageDraw.Draw(stain)
    for _ in range(10):
        cx = int(rng.integers(26, CBW - 26)); cy = int(rng.integers(26, CBH - 26))
        rx = int(rng.integers(34, 120)); ry = int(rng.integers(20, 64))
        col = tuple(int(v) for v in rng.choice([(158, 138, 106), (140, 122, 94), (170, 148, 116)]))
        sd.ellipse([cx - rx // 2, cy - ry // 2, cx + rx // 2, cy + ry // 2], fill=col)
    stain = stain.filter(ImageFilter.GaussianBlur(14))
    front = ImageChops.multiply(front, stain)
    sc = Image.new("RGB", (CBW, CBH), (0, 0, 0))
    sd = ImageDraw.Draw(sc)
    for _ in range(8):
        x0 = int(rng.integers(10, CBW - 60)); y0 = int(rng.integers(14, CBH - 30))
        dx = int(rng.integers(-40, 60)); dy = int(rng.integers(-10, 12))
        sd.line([x0, y0, x0 + dx, y0 + dy], fill=(150, 152, 148), width=1)
    sc = sc.filter(ImageFilter.GaussianBlur(1))
    front = ImageChops.screen(front, ImageEnhance.Brightness(sc).enhance(0.30))
    ew = Image.new("RGB", (CBW, CBH), (0, 0, 0))
    ImageDraw.Draw(ew).rounded_rectangle([MARGIN - 1, MARGIN - 1, CBW - MARGIN, CBH - MARGIN], radius=44,
                                         outline=(128, 130, 126), width=2)
    ew = ew.filter(ImageFilter.GaussianBlur(1))
    front = ImageChops.screen(front, ImageEnhance.Brightness(ew).enhance(0.22))
    arr = _np.asarray(front, dtype=_np.float32)
    arr += rng.normal(0.0, 3.0, arr.shape)
    front = Image.fromarray(_np.clip(arr, 0, 255).astype(_np.uint8))
    # === 内缘(真正的凹槽光影, 由"距洞口距离"光照函数产生) ===
    # 径向凹槽阴影 + 左上被上沿挡光更重 + 右下微微接光; 全程软渐变无硬线
    recess = Image.new("L", (CBW, CBH), 0)
    ImageDraw.Draw(recess).rounded_rectangle(
        [bezel_pad + HOLE_RIM - 30, bezel_pad + HOLE_RIM - 30,
         CBW - bezel_pad - HOLE_RIM + 29, CBH - bezel_pad - HOLE_RIM + 29],
        radius=40, fill=255)
    ImageDraw.Draw(recess).rounded_rectangle(
        [bezel_pad + HOLE_RIM - 4, bezel_pad + HOLE_RIM - 4,
         CBW - bezel_pad - HOLE_RIM + 3, CBH - bezel_pad - HOLE_RIM + 3],
        radius=26, fill=0)
    recess = recess.filter(ImageFilter.GaussianBlur(10))
    rec = _np.asarray(recess, dtype=_np.float32) / 255.0
    far = (xxm + yym) * 0.5               # 左上 0 -> 右下 1
    arr = _np.asarray(front, dtype=_np.float32)
    arr *= (1.0 - rec * (0.48 + 0.26 * (1.0 - far)))[:, :, None]   # 凹槽深度墙(左上重)
    arr += (rec * far * 16)[:, :, None]                             # 右下微微接光
    front = Image.fromarray(_np.clip(arr, 0, 255).astype(_np.uint8))
    # 统一画布级曲面洞几何: 前脸洞 = 屏幕可见区 = 缝隙线, 全部同一 warp 结果
    hole_cv = Image.new("L", (CBW, CBH), 0)
    ImageDraw.Draw(hole_cv).rounded_rectangle(
        [bezel_pad + HOLE_RIM, bezel_pad + HOLE_RIM,
         CBW - bezel_pad - HOLE_RIM - 1, CBH - bezel_pad - HOLE_RIM - 1],
        radius=30, fill=255)
    hole_cv = barrel_warp(hole_cv.convert("RGB"), edge_dark=0.0).convert("L")
    inner_cv = Image.new("L", (CBW, CBH), 0)
    ImageDraw.Draw(inner_cv).rounded_rectangle(
        [bezel_pad + HOLE_RIM + 6, bezel_pad + HOLE_RIM + 6,
         CBW - bezel_pad - HOLE_RIM - 7, CBH - bezel_pad - HOLE_RIM - 7],
        radius=26, fill=255)
    inner_cv = barrel_warp(inner_cv.convert("RGB"), edge_dark=0.0).convert("L")
    outer_cv = Image.new("L", (CBW, CBH), 0)
    ImageDraw.Draw(outer_cv).rounded_rectangle(
        [MARGIN, MARGIN, CBW - MARGIN - 1, CBH - MARGIN - 1], radius=44, fill=255)
    outer_cv = barrel_warp(outer_cv.convert("RGB"), edge_dark=0.0).convert("L")
    front_mask = ImageChops.subtract(outer_cv, hole_cv)   # 前脸 = 外圈 - 曲面洞
    front = Image.composite(front, Image.new("RGB", (CBW, CBH), TR_KEY), front_mask)
    # 电源 LED(前脸左下)
    ImageDraw.Draw(front).ellipse([bezel_pad + 6, CBH - 34, bezel_pad + 14, CBH - 26],
                                  fill=(90, 235, 110), outline=(30, 70, 40))

    # 屏幕侧"内陷"阴影: 洞口边缘往屏幕内落软阴影(玻璃沉入面板)
    # 凹槽内缘光照: 左上被上沿挡光更暗, 右下反射进光(与外壳方向相反)
    hm = Image.new("L", (W, H), 0)
    ImageDraw.Draw(hm).rounded_rectangle(
        [HOLE_RIM, HOLE_RIM, W - HOLE_RIM, H - HOLE_RIM], radius=36, fill=255)
    ImageDraw.Draw(hm).rounded_rectangle(
        [HOLE_RIM + 7, HOLE_RIM + 7, W - HOLE_RIM - 7, H - HOLE_RIM - 7],
        radius=28, fill=0)
    hm = hm.filter(ImageFilter.GaussianBlur(3))
    xxm_s, yym_s = _np.meshgrid(_np.linspace(0, 1, W, dtype=_np.float32),
                                _np.linspace(0, 1, H, dtype=_np.float32))
    dir_s = (xxm_s + yym_s) * 0.5
    hm_arr = _np.asarray(hm, dtype=_np.float32)
    sh_dark = Image.fromarray(
        (_np.clip(hm_arr * (1.0 - dir_s * 0.6), 0, 255)).astype(_np.uint8))
    hole_shade = Image.composite(
        Image.new("RGB", (W, H), (124, 132, 126)),
        Image.new("RGB", (W, H), (255, 255, 255)), sh_dark)
    hole_shade = barrel_warp(hole_shade, edge_dark=0.0)   # 与屏幕同一曲率

    # 洞口可见区域掩码(屏幕坐标系): 与前脸洞口完全同一几何(同半径/无blur),
    # 屏幕正好填满洞口, 不留主题色细缝
    # 洞口可见区域 = 画布级曲面洞裁到屏幕区(与前脸洞同一几何, 无误差细缝)
    hole_vis = hole_cv.crop((bezel_pad, bezel_pad, bezel_pad + W, bezel_pad + H))
    # 接缝缝隙线: 两个不同平面的交界 -> 同一几何的 6px 锐利环差(0模糊)

    # 轻微 3/4 透视(绘图手稿风格): 输出四角映射到输入四角(在画布内)。
    # 顶层略右倾、右侧略缩, 形成轻微"斜视"体感。
    def _persp_coeffs():
        w, h = CBW, CBH
        dst = [(0.0, 0.0), (w - 1.0, 0.0), (w - 1.0, h - 1.0), (0.0, h - 1.0)]
        # 输入图采样角点(轻微倾斜 + 右侧收窄 + 下方略带透视)
        src = [(16.0, 6.0), (w - 14.0, 14.0), (w - 20.0, h - 20.0), (4.0, h - 10.0)]
        A, b = [], []
        for (dx, dy), (sx, sy) in zip(dst, src):
            A.append([dx, dy, 1, 0, 0, 0, -dx * sx, -dy * sx]); b.append(sx)
            A.append([0, 0, 0, dx, dy, 1, -dx * sy, -dy * sy]); b.append(sy)
        return tuple(_np.linalg.solve(_np.array(A, float), _np.array(b, float)))

    PERSP = _persp_coeffs()

    def assemble(screen_img):
        """屏幕在内缘/外壳之下: 内陷阴影 -> 洞口裁剪 -> 只往洞口里贴。"""
        scr = ImageChops.multiply(screen_img, hole_shade)
        scr = Image.composite(scr, Image.new("RGB", (W, H), TR_KEY), hole_vis)
        out = front.copy()
        out.paste(scr, (bezel_pad, bezel_pad), hole_vis)
        # 整机轻微透视(所有层一起倾斜, 层间关系不变)
        return out.transform((CBW, CBH), Image.Transform.PERSPECTIVE, PERSP,
                             resample=Image.Resampling.BICUBIC,
                             fillcolor=TR_KEY)

    # ---- 边缘渐晕(预计算): 中心 255 -> 角落 0 ----
    vig = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vig)
    vd.ellipse([-int(W * 0.18), -int(H * 0.24), W + int(W * 0.18), H + int(H * 0.24)], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(90))
    vig = vig.point(lambda v: 150 + (v * 105) // 255)  # 弱渐晕: 角落最多 40% 压暗

    # 屏幕四角的圆角蒙版(平滑过渡, 不再硬切)
    corner_mask = Image.new("L", (W, H), 0)
    cmd_ = ImageDraw.Draw(corner_mask)
    cmd_.rounded_rectangle([0, 0, W - 1, H - 1], radius=44, fill=255)
    corner_mask = corner_mask.filter(ImageFilter.GaussianBlur(6))
    # 屏幕玻璃边界也做同一曲率畸变 -> 边缘是弧形(和内容共享同一曲面几何)
    corner_mask = barrel_warp(corner_mask.convert("RGB"), edge_dark=0.0).convert("L")
    screen_bg = Image.new("RGB", (W, H), (6, 12, 8))
    # 玻璃反光(左上柔光 + 右下微光, 参照实物照片)
    sheen = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(sheen)
    sd.ellipse([-int(W * 0.20), -int(H * 0.55), int(W * 0.46), int(H * 0.32)], fill=26)
    sd.ellipse([int(W * 0.62), int(H * 0.70), int(W * 1.08), int(H * 1.15)], fill=10)
    sheen = sheen.filter(ImageFilter.GaussianBlur(45))
    sheen_img = Image.new("RGB", (W, H), (232, 242, 236))

    def compose_screen(term, tframe):
        """终端帧(720x450, 1:1 原生字形) -> 完整仿真管线 -> 800x500 屏幕。
        主循环与闪烁段共用: 进度条和正文拿到完全相同的
        辉光/扫描线/渐晕/圆角/玻璃反光, 不会出现"两三秒后变锐利"的分层问题。
        零缩放: 字符像素不重采样, 不会缺胳膊少腿。"""
        screen = screen_bg.copy()
        screen.paste(term, ((W - TERM_W) // 2, (H - TERM_H) // 2))
        # 进度条模块与正文同层(画在条纹之下): 之后条纹/畸变/辉光对其同样生效
        if tframe >= MODULE_START:
            draw_shutdown_bar(screen, tframe, glow=False)
        # 扫描线(先画, 与内容/模块一起畸变): 物理上是"每4行亮度压暗",
        # 不是画新颜色线 -> 文字/模块/背景被遮挡程度一致且颜色不失真
        arr = _np.asarray(screen, dtype=_np.float32)
        arr[1::4, :, :] *= 0.76
        screen = Image.fromarray(_np.clip(arr, 0, 255).astype(_np.uint8))
        # 整屏(内容+模块+条纹+黑边)统一畸变, 再统一辉光
        img = barrel_warp(screen)
        glow = img.filter(ImageFilter.GaussianBlur(6))
        glow = ImageEnhance.Brightness(glow).enhance(0.85)
        img = ImageChops.screen(img, glow)
        # 渐晕 / 四角圆角 / 玻璃反光
        img = Image.composite(img, Image.new("RGB", (W, H), (2, 6, 3)), vig)
        img = Image.composite(img, screen_bg, corner_mask)
        img = Image.composite(sheen_img, img, sheen)
        return img

    n = 0
    frames_list = []
    last_term = None
    for f in files:
        n += 1
        term = Image.open(f).convert("RGB")
        last_term = term
        img = compose_screen(term, n)
        # --- 随机闪烁与温和的故障条纹(仅主循环) ---
        rnd = random.random()
        if rnd < 0.75:
            img = ImageEnhance.Brightness(img).enhance(1.0 + (rnd - 0.5) * 0.04)
        if rnd < 0.05:
            y0, hh = random.randint(0, H - 60), random.randint(3, 22)
            dr = random.randint(-8, 8)
            if dr:
                band = img.crop((0, y0, W, y0 + hh))
                shifted = Image.new("RGB", (W, hh), (6, 14, 8))
                shifted.paste(band, (dr, 0), None)
                if dr > 0:
                    shifted.paste(band, (dr - W, 0), None)
                img.paste(shifted, (0, y0))

        # --- 合入外壳(屏幕在面板下面) ---
        frames_list.append(assemble(img))

    # ---- 开机动画: 物理仿真(开机瞬间灯丝供电) ----
    # 显像管开机的真实过程: 扫描电路先出一根中央亮线 -> 光栅上下展开
    # (展开边缘是更亮的扫描线) -> 亮度过冲 -> 稳定为待机画面
    power_frames = []
    dark = assemble(Image.new("RGB", (W, H), (0, 0, 0)))
    yctr = H // 2
    power_frames += [dark, dark]

    def _line_screen(scr, y0, hh, edge=1.0):
        """竖条亮线(带辉光), 用于开机中央亮线与展开边缘。"""
        d = ImageDraw.Draw(scr)
        d.rectangle([0, int(y0), W, int(y0 + hh)],
                    fill=(int(150 * edge), int(255 * edge), int(130 * edge)))
        return scr.filter(ImageFilter.GaussianBlur(2))

    # 1) 中央亮线点亮(2帧, 亮度渐起)
    for k in range(2):
        scr = Image.new("RGB", (W, H), (0, 0, 0))
        scr = _line_screen(scr, yctr - 3, 6, edge=0.55 + 0.45 * k)
        scr = Image.composite(scr, screen_bg, corner_mask)
        power_frames.append(assemble(scr))

    # 2) 光栅上下展开(14帧: 已扫描区域是画面, 展开边缘保持亮线)
    for i in range(1, 15):
        hh = int(H * (i / 14) ** 0.6)
        top = int(yctr - hh / 2)
        scr = Image.new("RGB", (W, H), (0, 0, 0))
        d = ImageDraw.Draw(scr)
        # 已展开区域: 深绿底色(待机画面)
        d.rectangle([0, top, W, top + hh], fill=(10, 26, 14))
        # 展开边缘亮线(上下两道)
        d.rectangle([0, top + 2, W, top + 8], fill=(118, 235, 105))
        d.rectangle([0, top + hh - 9, W, top + hh - 3], fill=(118, 235, 105))
        scr = scr.filter(ImageFilter.GaussianBlur(1))
        scr = Image.composite(scr, screen_bg, corner_mask)
        power_frames.append(assemble(scr))

    # 3) 亮度过冲(2帧: 整屏微闪绿光再回落)
    for k in range(2):
        scr = Image.new("RGB", (W, H), (0, 0, 0))
        d = ImageDraw.Draw(scr)
        d.rectangle([0, 0, W, H], fill=(int(60 - k * 30), int(120 - k * 55), int(66 - k * 32)))
        scr = Image.composite(scr, screen_bg, corner_mask)
        power_frames.append(assemble(scr))

    # 4) 稳定待机(带扫描线且随曲率, 与打字开始前的状态一致)
    scr = Image.new("RGB", (W, H), (12, 28, 16))
    arr = _np.asarray(scr, dtype=_np.float32)
    arr[1::4, :, :] *= 0.72
    scr = Image.fromarray(_np.clip(arr, 0, 255).astype(_np.uint8))
    scr = Image.composite(scr, screen_bg, corner_mask)
    scr = barrel_warp(scr)
    f = assemble(scr)
    power_frames.append(f)

    # ---- 加载完成后: 老显示器式闪烁 10 秒(150帧 @15fps) ----
    # 屏幕内容带一条"刷新暗带"从顶部扫到底部(像电子束扫描),
    # 暗带前缘略亮、带体变暗; 其余时间部分帧静止(GIF 增量压缩), 偶发单线跳变
    import numpy as np
    flicker = []
    screen_rect = (bezel_pad, bezel_pad, bezel_pad + W, bezel_pad + H)
    rows = np.arange(H, dtype=np.float32)
    PERIOD = 28          # 每 ~1.9s 完成一次自上而下的扫掠
    BAND_H, FALL = 30.0, 115.0
    for i in range(150):
        rnd = random.random()
        phase = (i % PERIOD) / PERIOD
        y0 = phase * (H + FALL) - FALL / 2        # 暗带中心位置(屏外 -> 屏内 -> 屏外)
        # 每帧从终端帧重跑完整管线: 进度条持续增长且与正文同特效
        scr = compose_screen(last_term, 200 + i)
        # 每 4 帧扫 2 帧暗带(节奏感), 其余帧不动带子
        if i % 4 >= 2:
            arr = np.asarray(scr, dtype=np.float32)
            dark_alpha = np.exp(-((rows - y0) / BAND_H) ** 2) * 0.24        # 带体变暗
            lead_alpha = np.exp(-((rows - (y0 - FALL * 0.6)) / (BAND_H * 1.2)) ** 2) * 0.08  # 前缘略亮
            gain = 1.0 + lead_alpha[:, None, None] - dark_alpha[:, None, None]
            arr = np.clip(arr * gain, 0, 255)
            scr = Image.fromarray(arr.astype(np.uint8))
        f = assemble(scr)
        # 偶发一条随机扫描线跳变(保留一些随机感)
        if rnd < 0.10:
            dfx = ImageDraw.Draw(f)
            yl = random.randint(bezel_pad + 24, bezel_pad + H - 24)
            dfx.line([(bezel_pad, yl), (bezel_pad + W, yl)],
                     fill=random.choice([(70, 130, 80), (6, 16, 10)]))
        flicker.append(f)

    # ---- 息屏: 物理正确的 CRT 关机 ----
    # 关机瞬间扫描场停止 -> 画面垂直"塌缩"成中央一条亮线(能量聚集所以更亮)
    # -> 亮线轻微闪烁 -> 迅速熄灭。 不是逐渐变暗!
    # 塌缩源用闪烁段最后一帧(此时进度条已 100%)
    sleep = []
    source = flicker[-1]
    nl = 10
    for i in range(nl):
        s = 1.0 - i / (nl - 1)                 # 1 -> 0
        hh = max(3, int(H * (s ** 1.2)))
        sq = source.crop(screen_rect).resize((W, hh), Image.NEAREST)
        # 塌缩时保持/增强亮度: 亮度集中到越来越窄的线上
        scr = ImageEnhance.Brightness(sq).enhance(1.0 + 0.35 * (1 - s))
        full = Image.new("RGB", (W, H), (0, 0, 0))
        full.paste(scr, (0, (H - hh) // 2))
        full = Image.composite(full, screen_bg, corner_mask)
        sleep.append(assemble(full))
    # 中央亮线(磷光绿, 带辉光, 轻微闪烁)
    yctr = H // 2
    for i in range(6):
        lv = 255 if i % 2 == 0 else 230
        line = Image.new("RGB", (W, H), (0, 0, 0))
        ld = ImageDraw.Draw(line)
        ld.rectangle([0, yctr - 2, W, yctr + 2],
                     fill=(int(lv * 0.62), lv, int(lv * 0.50)))
        line = line.filter(ImageFilter.GaussianBlur(2))
        sleep.append(assemble(line))
    # 熄灭: 亮线快速衰减至消失
    for i in range(4):
        lv = int(255 * (1 - i / 3) ** 1.5)
        scr = Image.new("RGB", (W, H), (0, 0, 0))
        if lv > 6:
            ld = ImageDraw.Draw(scr)
            ld.rectangle([0, yctr - 2, W, yctr + 2],
                         fill=(int(lv * 0.62), lv, int(lv * 0.50)))
        sleep.append(assemble(scr))
    off = [dark] * 3

    all_frames = power_frames + frames_list + flicker + sleep + off
    for i, fr in enumerate(all_frames):
        fr.save(frames_out / f"seq_{i:04d}.png")
    source.save(frames_out / "base.png")  # 供编码器做共享调色板(100% 进度条画面)
    print(f"INFO: CRT frames: {len(all_frames)}")


# ---------------------------------------------------------------------------
# 5) ffmpeg 编码
# ---------------------------------------------------------------------------
def encode_gif(frames_dir: Path, out: Path) -> None:
    """Pillow 直编码 GIF: 共享调色板 + 无抖动量化。
    静态重复帧会被 GIF 增量编码压缩到极小, 是闪烁/停留段体积的关键。"""
    import re as _re
    import numpy as np

    files = sorted(
        frames_dir.glob("seq_*.png"),
        key=lambda p: int(_re.search(r"(\d+)", p.name).group(1)),
    )
    # 用信息最全的基帧建 256 色共享调色板
    pal_ref = Image.open(frames_dir / "base.png").convert("RGB")
    # Pillow 编码(P 模式共享调色板, optimize=True 增量压缩),
    # 之后二进制补丁: 写入器会重排调色板, 需在产物里重定位哨兵色并按 GCE 修补透明索引
    pal = pal_ref.quantize(colors=255, method=Image.Quantize.MEDIANCUT,
                           dither=Image.Dither.NONE)
    pal_list = list(pal.getpalette())[: 255 * 3] + [254, 0, 254]
    pal_img = Image.new("P", (1, 1))
    pal_img.putpalette(pal_list)

    frames = []
    for p in files:
        im = Image.open(p).convert("RGBA")
        # 先按哨兵色打回不透明, 量化统一调色板(这步保留 alpha 不用)
        rgb = im.convert("RGB")
        q = rgb.quantize(palette=pal_img, dither=Image.Dither.NONE)
        frames.append(q)

    duration = int(round(1000 / FPS))

    frames[0].save(
        out, save_all=True, append_images=frames[1:],
        optimize=True, duration=duration, loop=0,
    )
    print(f"INFO: encoded {len(frames)} frames -> {out}")


# ---------------------------------------------------------------------------
def main() -> None:
    import urllib.request

    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default=CONFIG["user"])
    ap.add_argument("--avatar", default=None, help="本地头像路径, 默认从 GitHub 下载")
    ap.add_argument("--theme", default="dark", choices=["dark", "light"],
                    help="机壳外填充的页面底色(dark #0d1117 / light #ffffff)")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    if args.out is None:
        args.out = str(Path(__file__).parent / "out" / f"banner_{args.theme}.gif")
    global THEME_BG
    THEME_BG = (13, 17, 23) if args.theme == "dark" else (255, 255, 255)

    WORK.mkdir(parents=True, exist_ok=True)
    FRAMES_IN.mkdir(parents=True, exist_ok=True)
    if args.avatar:
        avatar_src = Path(args.avatar)
    else:
        avatar_src = WORK / "avatar.png"
        urllib.request.urlretrieve(f"https://github.com/{args.user}.png?size=460", avatar_src)

    avatar_px = WORK / "avatar_px.png"
    pixelate_avatar(avatar_src, avatar_px)

    old = os.getcwd()
    os.chdir(WORK)  # gifos 的 frames/ 与 output.gif 相对当前目录
    need = not any(FRAMES_IN.iterdir())
    if need:
        gen_terminal_frames(avatar_px)
    os.chdir(old)

    crt_post_process(FRAMES_IN, FRAMES_OUT)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    encode_gif(FRAMES_OUT, out)
    print(f"INFO: done -> {out}")


if __name__ == "__main__":
    main()
