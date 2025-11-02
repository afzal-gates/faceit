"""
Generate professional-looking reference images with enhanced 3D-style head models.
Creates more realistic anatomical references similar to professional stock images.
"""

import os
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL/Pillow not available. Please install: pip install Pillow")


def create_gradient(draw, x1, y1, x2, y2, start_color, end_color):
    """Create a simple gradient effect."""
    for i, y in enumerate(range(y1, y2)):
        ratio = i / (y2 - y1)
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        draw.line([(x1, y), (x2, y)], fill=(r, g, b))


def draw_3d_sphere(draw, cx, cy, radius, base_color):
    """Draw a sphere with 3D shading effect."""
    # Multiple layers for smooth shading
    for r in range(radius, 0, -1):
        # Calculate shade based on distance from center
        shade_factor = r / radius

        # Lighter towards top-left (light source)
        offset_x = int((radius - r) * 0.3)
        offset_y = int((radius - r) * 0.3)

        # Adjust color
        adjusted_color = tuple(
            min(255, int(c * (0.5 + shade_factor * 0.5)))
            for c in base_color
        )

        draw.ellipse([
            cx - r + offset_x, cy - r + offset_y,
            cx + r + offset_x, cy + r + offset_y
        ], fill=adjusted_color, outline=adjusted_color)


def create_professional_reference(width, height, landmarks, title, output_path, draw_3d_head):
    """Create professional reference with 3D-style head model."""
    if not PIL_AVAILABLE:
        return False

    # Create image with gradient background
    img = Image.new('RGB', (width, height), '#e8e8e8')
    draw = ImageDraw.Draw(img)

    # Subtle gradient background
    create_gradient(draw, 0, 0, width, height, (240, 240, 245), (220, 220, 230))

    # Try to load fonts
    try:
        font_title = ImageFont.truetype("arial.ttf", 32)
        font_label = ImageFont.truetype("arial.ttf", 14)
    except:
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()

    # Draw 3D head model
    if draw_3d_head:
        draw_3d_head(draw, width, height)

    # Draw title with shadow
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    title_y = 25

    # Shadow
    draw.text((title_x + 2, title_y + 2), title, fill='#888888', font=font_title)
    # Title
    draw.text((title_x, title_y), title, fill='#2a2a2a', font=font_title)

    # Draw landmarks with 3D effect
    for x, y, label, color in landmarks:
        # Draw shadow
        shadow_offset = 3
        draw.ellipse([x - 10 + shadow_offset, y - 10 + shadow_offset,
                     x + 10 + shadow_offset, y + 10 + shadow_offset],
                    fill='#00000040')

        # Draw white outline
        draw.ellipse([x - 11, y - 11, x + 11, y + 11],
                    fill='white', outline='#666666', width=2)

        # Draw colored point with 3D effect
        color_rgb = {
            'red': (220, 50, 50),
            'green': (50, 180, 50),
            'blue': (50, 120, 220),
            'purple': (160, 80, 200),
            'darkgreen': (40, 120, 40),
            'darkblue': (40, 80, 160),
            'darkred': (150, 30, 30),
        }.get(color, (128, 128, 128))

        draw_3d_sphere(draw, x, y, 8, color_rgb)

        # Draw label with professional styling
        label_bbox = draw.textbbox((0, 0), label, font=font_label)
        label_width = label_bbox[2] - label_bbox[0]
        label_height = label_bbox[3] - label_bbox[1]

        label_x = x + 15
        label_y = y - label_height // 2

        # Label shadow
        padding = 4
        draw.rectangle([label_x - padding + 1, label_y - padding + 1,
                       label_x + label_width + padding + 1, label_y + label_height + padding + 1],
                      fill='#00000030')

        # Label background with gradient
        draw.rectangle([label_x - padding, label_y - padding,
                       label_x + label_width + padding, label_y + label_height + padding],
                      fill='white', outline='#999999', width=1)

        # Label text
        draw.text((label_x, label_y), label, fill='#2a2a2a', font=font_label)

    # Apply slight blur for anti-aliasing (optional)
    # img = img.filter(ImageFilter.SMOOTH)

    # Save
    img.save(output_path, quality=95)
    print(f"Created: {output_path}")
    return True


def draw_face_outline_3d(draw, width, height):
    """Draw 3D-style full head model for face outline."""
    center_x = width // 2
    face_top = 180
    face_bottom = 900

    # Base head shape with shading
    head_points = [
        (center_x, face_bottom),
        (center_x + 40, face_bottom - 50),
        (center_x + 90, face_bottom - 130),
        (center_x + 140, face_bottom - 230),
        (center_x + 180, face_bottom - 350),
        (center_x + 210, face_bottom - 480),
        (center_x + 225, face_bottom - 600),
        (center_x + 230, face_bottom - 710),
        (center_x + 210, face_top + 30),
        (center_x + 170, face_top - 10),
        (center_x + 110, face_top - 35),
        (center_x + 40, face_top - 50),
        (center_x, face_top - 55),
        (center_x - 40, face_top - 50),
        (center_x - 110, face_top - 35),
        (center_x - 170, face_top - 10),
        (center_x - 210, face_top + 30),
        (center_x - 230, face_bottom - 710),
        (center_x - 225, face_bottom - 600),
        (center_x - 210, face_bottom - 480),
        (center_x - 180, face_bottom - 350),
        (center_x - 140, face_bottom - 230),
        (center_x - 90, face_bottom - 130),
        (center_x - 40, face_bottom - 50),
    ]

    # Draw filled head with gradient-like shading
    draw.polygon(head_points, fill='#f5d5c0', outline='#d4a574', width=4)

    # Add subtle shading on left side (shadow)
    shadow_points = [
        (center_x - 230, face_bottom - 710),
        (center_x - 225, face_bottom - 600),
        (center_x - 210, face_bottom - 480),
        (center_x - 180, face_bottom - 350),
        (center_x - 140, face_bottom - 230),
        (center_x - 100, face_bottom - 130),
        (center_x - 100, face_bottom - 600),
    ]
    draw.polygon(shadow_points, fill='#00000015')

    # Eyes
    draw.ellipse([center_x - 100, 400, center_x - 40, 445],
                fill='white', outline='#b8936d', width=3)
    draw.ellipse([center_x - 80, 410, center_x - 60, 435], fill='#4a90c0')
    draw.ellipse([center_x - 75, 415, center_x - 65, 430], fill='#2a2a2a')

    draw.ellipse([center_x + 40, 400, center_x + 100, 445],
                fill='white', outline='#b8936d', width=3)
    draw.ellipse([center_x + 60, 410, center_x + 80, 435], fill='#4a90c0')
    draw.ellipse([center_x + 65, 415, center_x + 75, 430], fill='#2a2a2a')

    # Eyebrows
    draw.arc([center_x - 110, 350, center_x - 30, 390], 20, 160, fill='#8b6f47', width=7)
    draw.arc([center_x + 30, 350, center_x + 110, 390], 20, 160, fill='#8b6f47', width=7)

    # Nose with shading
    nose_points = [
        (center_x, 420),
        (center_x - 8, 520),
        (center_x - 30, 575),
        (center_x, 585),
        (center_x + 30, 575),
        (center_x + 8, 520),
    ]
    draw.polygon(nose_points, fill='#ead5be', outline='#d4a574', width=2)

    # Nostrils
    draw.ellipse([center_x - 35, 565, center_x - 20, 580], fill='#8b6f47')
    draw.ellipse([center_x + 20, 565, center_x + 35, 580], fill='#8b6f47')

    # Mouth
    mouth_points = [
        (center_x - 80, 700),
        (center_x - 50, 685),
        (center_x - 20, 680),
        (center_x, 678),
        (center_x + 20, 680),
        (center_x + 50, 685),
        (center_x + 80, 700),
    ]
    draw.line(mouth_points, fill='#c96a72', width=5, joint='curve')

    mouth_bottom = [
        (center_x + 80, 700),
        (center_x + 50, 720),
        (center_x + 20, 728),
        (center_x, 730),
        (center_x - 20, 728),
        (center_x - 50, 720),
        (center_x - 80, 700),
    ]
    draw.line(mouth_bottom, fill='#b85a62', width=5, joint='curve')


def generate_all_professional():
    """Generate all reference images with professional 3D-style."""

    images_config = [
        {
            'name': 'face_outline.png',
            'title': 'Face Outline (17 Points)',
            'width': 800,
            'height': 1000,
            'draw_func': draw_face_outline_3d,
            'landmarks': [
                (400, 900, "0: Chin", "red"),
                (420, 850, "1", "blue"),
                (450, 790, "2", "blue"),
                (485, 720, "3", "blue"),
                (520, 640, "4", "blue"),
                (550, 550, "5", "blue"),
                (575, 450, "6", "blue"),
                (590, 340, "7", "blue"),
                (595, 230, "8", "blue"),
                (205, 230, "16", "green"),
                (210, 340, "15", "green"),
                (225, 450, "14", "green"),
                (250, 550, "13", "green"),
                (280, 640, "12", "green"),
                (315, 720, "11", "green"),
                (350, 790, "10", "green"),
                (380, 850, "9", "green"),
            ]
        },
        # Add more configurations for other features...
    ]

    script_dir = Path(__file__).parent

    for config in images_config:
        print(f"Generating {config['name']}...")
        output_path = script_dir / config['name']
        create_professional_reference(
            config['width'],
            config['height'],
            config['landmarks'],
            config['title'],
            output_path,
            config['draw_func']
        )


if __name__ == "__main__":
    print("Generating Professional 3D-Style Reference Images...")
    print("=" * 60)

    if not PIL_AVAILABLE:
        print("ERROR: PIL/Pillow required. Install: pip install Pillow")
    else:
        generate_all_professional()
        print("\nDone!")
