import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

MEDIA_DIR = "media/products"
os.makedirs(MEDIA_DIR, exist_ok=True)

def create_ceramic_image(filename, title, category_tag, bg_color=(250, 247, 242), shape_type="vase", primary_color=(220, 205, 185), accent_color=(190, 150, 120)):
    w, h = 800, 1000
    img = Image.new('RGB', (w, h), bg_color)
    draw = ImageDraw.Draw(img)

    # 1. Subtle warm background gradient / studio floor
    for y in range(h):
        factor = y / h
        r = int(bg_color[0] - factor * 15)
        g = int(bg_color[1] - factor * 18)
        b = int(bg_color[2] - factor * 22)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Studio table surface line
    table_y = 750
    draw.rectangle([0, table_y, w, h], fill=(232, 222, 208))
    # Subtle wood grain or edge shadow
    draw.line([(0, table_y), (w, table_y)], fill=(205, 192, 175), width=3)
    for i in range(15):
        shadow_y = table_y + i
        alpha = int(30 * (1 - i / 15))
        draw.line([(0, shadow_y), (w, shadow_y)], fill=(215 - alpha, 205 - alpha, 192 - alpha))

    # 2. Draw soft drop shadow for the ceramic piece
    shadow_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_img)
    s_draw.ellipse([260, table_y - 25, 540, table_y + 40], fill=(80, 60, 45, 90))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=25))
    img.paste(shadow_img, (0, 0), shadow_img)

    # 3. Draw the Ceramic Piece on separate RGBA layer for lighting & highlights
    piece = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(piece)

    cx, cy = w // 2, 520

    if shape_type == "donut_vase":
        # Sculptural Donut Vase
        outer_r = 180
        inner_r = 80
        neck_w, neck_h = 70, 90
        # Neck
        p_draw.rectangle([cx - neck_w//2, cy - outer_r - neck_h + 20, cx + neck_w//2, cy - outer_r + 20], fill=primary_color + (255,))
        # Donut body
        p_draw.ellipse([cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r], fill=primary_color + (255,))
        # Donut hole
        p_draw.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r], fill=bg_color + (255,))
        # Highlight rim
        p_draw.ellipse([cx - neck_w//2, cy - outer_r - neck_h + 10, cx + neck_w//2, cy - outer_r - neck_h + 30], fill=accent_color + (255,))

    elif shape_type == "fluted_vase":
        # Fluted amphora / bud vase
        pts = [
            (cx - 30, cy - 220), (cx + 30, cy - 220),  # rim
            (cx + 40, cy - 140), (cx + 140, cy - 40),  # shoulder
            (cx + 110, cy + 120), (cx + 70, cy + 220), # body to base
            (cx - 70, cy + 220), (cx - 110, cy + 120),
            (cx - 140, cy - 40), (cx - 40, cy - 140),
        ]
        p_draw.polygon(pts, fill=primary_color + (255,))
        # Vertical fluting ribs
        for ox in range(-100, 110, 25):
            p_draw.line([(cx + ox * 0.4, cy - 120), (cx + ox, cy + 160)], fill=accent_color + (90,), width=4)
        # Lip
        p_draw.ellipse([cx - 35, cy - 230, cx + 35, cy - 210], fill=accent_color + (255,))

    elif shape_type == "bud_vase":
        # Mini bud vase with botanical sprig (matching image)
        pts = [
            (cx - 20, cy - 120), (cx + 20, cy - 120),
            (cx + 25, cy - 60), (cx + 95, cy + 30),
            (cx + 80, cy + 160), (cx + 50, cy + 210),
            (cx - 50, cy + 210), (cx - 80, cy + 160),
            (cx - 95, cy + 30), (cx - 25, cy - 60),
        ]
        p_draw.polygon(pts, fill=primary_color + (255,))
        # Botanical stem coming out
        b_draw = ImageDraw.Draw(piece)
        b_draw.line([(cx, cy - 110), (cx + 15, cy - 260)], fill=(75, 95, 60, 240), width=4)
        b_draw.line([(cx + 5, cy - 170), (cx - 40, cy - 230)], fill=(85, 105, 70, 220), width=3)
        b_draw.line([(cx + 10, cy - 200), (cx + 60, cy - 240)], fill=(85, 105, 70, 220), width=3)
        # Leaves & tiny white blossoms
        for lx, ly in [(cx + 15, cy - 260), (cx - 40, cy - 230), (cx + 60, cy - 240), (cx - 20, cy - 250), (cx + 40, cy - 270)]:
            b_draw.ellipse([lx - 12, ly - 8, lx + 12, ly + 8], fill=(95, 115, 75, 230))
            b_draw.ellipse([lx - 4, ly - 12, lx + 4, ly - 4], fill=(255, 255, 245, 250))

    elif shape_type == "pencil_cup":
        # Minimalist desk organizer cup with colored pencils (as in photo)
        p_draw.rectangle([cx - 70, cy - 50, cx + 70, cy + 210], fill=primary_color + (255,))
        p_draw.ellipse([cx - 70, cy - 65, cx + 70, cy - 35], fill=accent_color + (255,))
        # Pencils sticking out
        colors = [(40, 40, 40), (190, 140, 50), (160, 70, 60), (230, 220, 200)]
        angles = [-25, -10, 10, 22]
        for idx, (col, ang) in enumerate(zip(colors, angles)):
            px = cx + ang * 2
            p_draw.line([(px, cy - 40), (px + ang, cy - 180)], fill=col + (255,), width=8)
            # Pencil tip
            p_draw.polygon([(px + ang - 4, cy - 180), (px + ang + 4, cy - 180), (px + ang, cy - 200)], fill=(225, 200, 160, 255))
            p_draw.polygon([(px + ang - 2, cy - 193), (px + ang + 2, cy - 193), (px + ang, cy - 200)], fill=(30, 30, 30, 255))

    elif shape_type == "mushroom_lamp":
        # Ceramic Mushroom Lamp
        # Shade
        p_draw.chord([cx - 160, cy - 170, cx + 160, cy + 40], 180, 360, fill=primary_color + (255,))
        # Base stem
        p_draw.polygon([(cx - 45, cy - 10), (cx + 45, cy - 10), (cx + 65, cy + 210), (cx - 65, cy + 210)], fill=accent_color + (255,))
        # Warm ambient glow under shade
        glow = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        g_draw = ImageDraw.Draw(glow)
        g_draw.ellipse([cx - 140, cy - 30, cx + 140, cy + 90], fill=(255, 220, 130, 140))
        glow = glow.filter(ImageFilter.GaussianBlur(radius=20))
        piece.paste(glow, (0, 0), glow)

    elif shape_type == "wallmate":
        # Woven Wallmate & Ceramic beads
        # Wood dowel
        p_draw.rectangle([cx - 150, cy - 200, cx + 150, cy - 185], fill=(180, 140, 100, 255))
        # Hanging cord
        p_draw.line([(cx - 130, cy - 200), (cx, cy - 270)], fill=(220, 210, 190, 255), width=3)
        p_draw.line([(cx + 130, cy - 200), (cx, cy - 270)], fill=(220, 210, 190, 255), width=3)
        # Woven fringe & ceramic terracotta discs
        for x in range(cx - 120, cx + 125, 12):
            length = random.randint(180, 320)
            p_draw.line([(x, cy - 185), (x, cy - 185 + length)], fill=(235, 225, 210, 220), width=4)
        # Ceramic discs
        p_draw.ellipse([cx - 45, cy - 120, cx + 45, cy - 30], fill=primary_color + (255,))
        p_draw.ellipse([cx - 30, cy + 20, cx + 30, cy + 80], fill=accent_color + (255,))

    elif shape_type == "matcha_bowl":
        # Organic Wabi-Sabi Tea Bowl
        p_draw.chord([cx - 140, cy - 60, cx + 140, cy + 180], 0, 180, fill=primary_color + (255,))
        p_draw.ellipse([cx - 140, cy - 90, cx + 140, cy - 30], fill=accent_color + (255,))
        p_draw.rectangle([cx - 60, cy + 140, cx + 60, cy + 170], fill=accent_color + (255,))

    elif shape_type == "ceramic_mug":
        # Fluted mug with handle
        p_draw.rectangle([cx - 90, cy - 100, cx + 50, cy + 150], fill=primary_color + (255,))
        # Rim
        p_draw.ellipse([cx - 90, cy - 125, cx + 50, cy - 75], fill=accent_color + (255,))
        # Handle
        p_draw.arc([cx + 20, cy - 60, cx + 110, cy + 110], 270, 90, fill=accent_color + (255,), width=22)

    elif shape_type == "incense_arch":
        # Sculptural Arch Incense Burner
        p_draw.arc([cx - 120, cy - 160, cx + 120, cy + 120], 180, 360, fill=primary_color + (255,), width=48)
        p_draw.rectangle([cx - 120, cy - 20, cx - 72, cy + 180], fill=primary_color + (255,))
        p_draw.rectangle([cx + 72, cy - 20, cx + 120, cy + 180], fill=primary_color + (255,))
        p_draw.rectangle([cx - 160, cy + 170, cx + 160, cy + 200], fill=accent_color + (255,))

    else:
        # Classic Moon Jar / Stoneware Pot
        p_draw.ellipse([cx - 150, cy - 130, cx + 150, cy + 170], fill=primary_color + (255,))
        p_draw.ellipse([cx - 70, cy - 160, cx + 70, cy - 110], fill=accent_color + (255,))

    # Add realistic ceramic speckles / mineral texture
    p_pixels = piece.load()
    for _ in range(3500):
        sx = random.randint(0, w - 1)
        sy = random.randint(0, h - 1)
        if p_pixels[sx, sy][3] > 100:  # If inside ceramic body
            gray = random.randint(70, 110)
            p_pixels[sx, sy] = (gray, gray - 10, gray - 20, random.randint(90, 200))

    img.paste(piece, (0, 0), piece)

    # 4. Vignette / Soft Lighting effect
    lighting = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    l_draw = ImageDraw.Draw(lighting)
    l_draw.ellipse([cx - 300, 50, cx + 300, 650], fill=(255, 248, 235, 35))
    lighting = lighting.filter(ImageFilter.GaussianBlur(radius=50))
    img.paste(lighting, (0, 0), lighting)

    img.save(os.path.join(MEDIA_DIR, filename), quality=92)
    print(f"Generated {filename}")

# Generate catalog images
items = [
    ("donut_vase.jpg", "Wabi-Sabi Sandstone Donut Vase", "Vases", (248, 244, 238), "donut_vase", (215, 198, 178), (185, 168, 148)),
    ("moon_jar.jpg", "Arcadia Moon Jar in Speckled Oatmeal", "Vases", (246, 242, 236), "pot", (228, 220, 206), (200, 190, 175)),
    ("fluted_amphora.jpg", "Sculptural Ribbed Amphora Vase", "Vases", (250, 246, 240), "fluted_vase", (195, 125, 95), (170, 100, 75)),
    ("bud_vase.jpg", "Aura Fluted Bud Vase with Botanical Sprig", "Vases", (249, 246, 242), "bud_vase", (242, 236, 226), (218, 210, 198)),
    ("desk_cup.jpg", "Cylindrical Oatmeal Ceramic Pen Holder", "Desk Decor", (250, 248, 244), "pencil_cup", (238, 232, 220), (210, 202, 188)),
    ("mushroom_lamp.jpg", "Kumo Ceramic Mushroom Lamp", "Lighting", (245, 241, 235), "mushroom_lamp", (230, 215, 195), (195, 140, 105)),
    ("wallmate_tapestry.jpg", "Handwoven Botanical Tapestry Wallmate", "Wall Decor", (248, 245, 240), "wallmate", (205, 120, 85), (160, 90, 60)),
    ("matcha_bowl.jpg", "Hand-pinched Wabi-Sabi Matcha Bowl", "Tableware", (246, 243, 238), "matcha_bowl", (125, 140, 120), (105, 120, 100)),
    ("fluted_mug.jpg", "Fluted Ceramic Mug with Sand Glaze", "Tableware", (249, 246, 241), "ceramic_mug", (220, 205, 185), (185, 168, 148)),
    ("incense_arch.jpg", "Zenith Stoneware Incense Arch", "Desk Decor", (247, 244, 239), "incense_arch", (200, 130, 95), (170, 105, 75)),
]

for filename, title, cat, bg, st, p_col, a_col in items:
    create_ceramic_image(filename, title, cat, bg, st, p_col, a_col)

print("All ceramic studio images generated successfully!")
