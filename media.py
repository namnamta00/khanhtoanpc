from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps


def font(size, bold=False):
    path = Path('C:/Windows/Fonts') / ('arialbd.ttf' if bold else 'arial.ttf')
    return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default(size=size)


def wrap(draw, text, face, width, max_lines):
    lines = []
    line = ''
    for word in text.split():
        candidate = (line + ' ' + word).strip()
        if draw.textlength(candidate, font=face) > width and line:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][:max(1, len(lines[-1]) - 3)] + '…'
    return '\n'.join(lines)


def card(product, extra, target, index=0, source=None):
    palettes = [('#101e35', '#55e5c5'), ('#201838', '#c8a6ff'), ('#152e39', '#7ad7ff')]
    bg, accent = palettes[index % len(palettes)]
    image = Image.new('RGB', (1080, 1080), bg)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((55, 55, 1025, 135), radius=20, fill=accent)
    draw.text((85, 74), 'KHÁNH TOÀN COMPUTER', font=font(38, True), fill=bg)
    title = wrap(draw, product.name, font(47, True), 920, 3)
    draw.multiline_text((70, 170), title, font=font(47, True), fill='white', spacing=10)
    if source:
        with Image.open(source) as original:
            photo = ImageOps.contain(ImageOps.exif_transpose(original).convert('RGB'), (900, 360))
        image.paste(photo, ((1080 - photo.width) // 2, 375 + (360 - photo.height) // 2))
    else:
        detail = wrap(draw, product.description or extra or 'Liên hệ để được tư vấn cấu hình phù hợp', font(33), 870, 6)
        draw.rounded_rectangle((65, 370, 1015, 755), radius=26, fill='#25364c')
        draw.multiline_text((100, 410), detail, font=font(33), fill='white', spacing=16)
    draw.text((70, 800), product.price or 'LIÊN HỆ BÁO GIÁ', font=font(49, True), fill=accent)
    draw.text((70, 886), 'Nhắn tin để xác nhận giá và tình trạng hàng', font=font(29), fill='white')
    draw.text((70, 957), 'facebook.com/khanhtoancomputer', font=font(29), fill=accent)
    image.save(target, 'PNG')
    return str(target)


def slideshow(photos, target, variant=0):
    import imageio.v2 as imageio
    import numpy as np
    if not photos:
        raise ValueError('Cần ít nhất một ảnh để tạo video.')
    order = list(photos[variant % len(photos):]) + list(photos[:variant % len(photos)])
    with imageio.get_writer(str(target), fps=24, codec='libx264', quality=8,
                           macro_block_size=2, ffmpeg_log_level='error') as writer:
        for path in order:
            with Image.open(path) as image:
                base = ImageOps.fit(image.convert('RGB'), (720, 720))
            for frame in range(72):
                inset = int(frame * 0.20)
                view = base.crop((inset, inset, 720-inset, 720-inset)).resize((720, 720))
                writer.append_data(np.asarray(view))
    return str(target)
