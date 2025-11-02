"""
Generate reference images for manual landmark picker.
Creates labeled diagrams showing landmark positions.
"""

import os
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL/Pillow not available. Please install: pip install Pillow")


def create_reference_image(width, height, landmarks, title, output_path, draw_guide=None):
    """
    Create a reference image with labeled landmark points.

    Args:
        width, height: Image dimensions
        landmarks: List of (x, y, label, color) tuples
        title: Image title
        output_path: Where to save the image
        draw_guide: Optional function to draw anatomical guides
    """
    if not PIL_AVAILABLE:
        return False

    # Create image with light gray background
    img = Image.new('RGB', (width, height), '#f0f0f0')
    draw = ImageDraw.Draw(img)

    # Try to load a font, fallback to default if not available
    try:
        font_title = ImageFont.truetype("arial.ttf", 28)
        font_label = ImageFont.truetype("arial.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except:
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw title
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, 20), title, fill='black', font=font_title)

    # Draw anatomical guide if provided
    if draw_guide:
        draw_guide(draw)

    # Draw landmarks
    for x, y, label, color in landmarks:
        # Draw point
        point_size = 8
        draw.ellipse([x - point_size, y - point_size, x + point_size, y + point_size],
                     fill=color, outline='black', width=2)

        # Draw label with background
        label_bbox = draw.textbbox((0, 0), label, font=font_small)
        label_width = label_bbox[2] - label_bbox[0]
        label_height = label_bbox[3] - label_bbox[1]

        # Position label to avoid overlap
        label_x = x + 12
        label_y = y - label_height // 2

        # Draw label background
        padding = 2
        draw.rectangle([label_x - padding, label_y - padding,
                       label_x + label_width + padding, label_y + label_height + padding],
                      fill='white', outline='gray', width=1)

        # Draw label text
        draw.text((label_x, label_y), label, fill='black', font=font_small)

    # Save image
    img.save(output_path)
    print(f"Created: {output_path}")
    return True


def generate_face_outline():
    """Generate face outline reference image (17 points)."""
    width, height = 800, 1000
    landmarks = []

    # Face outline from chin center around jaw to temples
    # Center chin (0)
    center_x = width // 2
    face_top = 200
    face_bottom = 850
    jaw_width = 280

    points = [
        (center_x, face_bottom, "0: Chin Center", "red"),
        # Right side (1-8)
        (center_x + 40, face_bottom - 50, "1", "blue"),
        (center_x + 80, face_bottom - 110, "2", "blue"),
        (center_x + 120, face_bottom - 180, "3", "blue"),
        (center_x + 160, face_bottom - 260, "4", "blue"),
        (center_x + 190, face_bottom - 350, "5", "blue"),
        (center_x + 210, face_bottom - 450, "6", "blue"),
        (center_x + 220, face_bottom - 550, "7", "blue"),
        (center_x + 220, face_bottom - 650, "8", "blue"),
        # Left side (9-16)
        (center_x - 220, face_bottom - 650, "16", "green"),
        (center_x - 220, face_bottom - 550, "15", "green"),
        (center_x - 210, face_bottom - 450, "14", "green"),
        (center_x - 190, face_bottom - 350, "13", "green"),
        (center_x - 160, face_bottom - 260, "12", "green"),
        (center_x - 120, face_bottom - 180, "11", "green"),
        (center_x - 80, face_bottom - 110, "10", "green"),
        (center_x - 40, face_bottom - 50, "9", "green"),
    ]

    def draw_face_guide(draw):
        """Draw face outline guide."""
        # Draw head shape
        head_outline = [
            (center_x, face_bottom),
            (center_x + 40, face_bottom - 50),
            (center_x + 80, face_bottom - 110),
            (center_x + 120, face_bottom - 180),
            (center_x + 160, face_bottom - 260),
            (center_x + 190, face_bottom - 350),
            (center_x + 210, face_bottom - 450),
            (center_x + 220, face_bottom - 550),
            (center_x + 220, face_bottom - 650),
            (center_x + 200, face_top + 20),
            (center_x + 150, face_top - 20),
            (center_x + 80, face_top - 40),
            (center_x, face_top - 50),
            (center_x - 80, face_top - 40),
            (center_x - 150, face_top - 20),
            (center_x - 200, face_top + 20),
            (center_x - 220, face_bottom - 650),
            (center_x - 220, face_bottom - 550),
            (center_x - 210, face_bottom - 450),
            (center_x - 190, face_bottom - 350),
            (center_x - 160, face_bottom - 260),
            (center_x - 120, face_bottom - 180),
            (center_x - 80, face_bottom - 110),
            (center_x - 40, face_bottom - 50),
            (center_x, face_bottom),
        ]
        draw.polygon(head_outline, fill='#ffe8d6', outline='#8b7355', width=3)

        # Draw simple facial features for context
        # Eyes
        draw.ellipse([center_x - 90, face_top + 160, center_x - 40, face_top + 190],
                     outline='#8b7355', width=2)
        draw.ellipse([center_x + 40, face_top + 160, center_x + 90, face_top + 190],
                     outline='#8b7355', width=2)
        # Nose
        draw.line([center_x, face_top + 200, center_x, face_top + 280], fill='#8b7355', width=2)
        # Mouth
        draw.arc([center_x - 60, face_top + 320, center_x + 60, face_top + 370],
                 0, 180, fill='#8b7355', width=2)

    output = Path(__file__).parent / "face_outline.png"
    return create_reference_image(width, height, points, "Face Outline (17 Points)", output, draw_face_guide)


def generate_eyebrows():
    """Generate eyebrows reference image (10 points)."""
    width, height = 800, 600

    # Left eyebrow (5 points) - Green
    left_brow_y = 250
    left_brow_start_x = 200
    points = [
        (left_brow_start_x, left_brow_y, "L Outer", "green"),
        (left_brow_start_x + 50, left_brow_y - 10, "L Outer Mid", "green"),
        (left_brow_start_x + 100, left_brow_y - 15, "L Center", "green"),
        (left_brow_start_x + 150, left_brow_y - 10, "L Inner Mid", "green"),
        (left_brow_start_x + 200, left_brow_y, "L Inner", "green"),
    ]

    # Right eyebrow (5 points) - Blue
    right_brow_y = 250
    right_brow_start_x = 430
    points.extend([
        (right_brow_start_x, right_brow_y, "R Inner", "blue"),
        (right_brow_start_x + 50, right_brow_y - 10, "R Inner Mid", "blue"),
        (right_brow_start_x + 100, right_brow_y - 15, "R Center", "blue"),
        (right_brow_start_x + 150, right_brow_y - 10, "R Outer Mid", "blue"),
        (right_brow_start_x + 200, right_brow_y, "R Outer", "blue"),
    ])

    def draw_eyebrows_guide(draw):
        """Draw eyebrows and face context."""
        center_x = width // 2
        # Upper face outline
        draw.arc([50, 80, 750, 520], 0, 180, fill='#8b7355', width=3)

        # Left eyebrow shape
        left_brow_curve = [
            (left_brow_start_x, left_brow_y),
            (left_brow_start_x + 50, left_brow_y - 10),
            (left_brow_start_x + 100, left_brow_y - 15),
            (left_brow_start_x + 150, left_brow_y - 10),
            (left_brow_start_x + 200, left_brow_y),
        ]
        draw.line(left_brow_curve, fill='#8b7355', width=8, joint='curve')

        # Right eyebrow shape
        right_brow_curve = [
            (right_brow_start_x, right_brow_y),
            (right_brow_start_x + 50, right_brow_y - 10),
            (right_brow_start_x + 100, right_brow_y - 15),
            (right_brow_start_x + 150, right_brow_y - 10),
            (right_brow_start_x + 200, right_brow_y),
        ]
        draw.line(right_brow_curve, fill='#8b7355', width=8, joint='curve')

        # Draw eyes for context
        draw.ellipse([220, 310, 380, 360], outline='#8b7355', width=2)
        draw.ellipse([420, 310, 580, 360], outline='#8b7355', width=2)

        # Nose bridge
        draw.line([center_x, 380, center_x, 460], fill='#8b7355', width=2)

    output = Path(__file__).parent / "eyebrows.png"
    return create_reference_image(width, height, points, "Eyebrows (10 Points)", output, draw_eyebrows_guide)


def generate_eyes():
    """Generate eyes reference image (12 points)."""
    width, height = 800, 600

    # Left eye (6 points) - Green
    left_eye_center_x = 280
    left_eye_y = 300
    eye_width = 80
    eye_height = 35

    points = [
        (left_eye_center_x - eye_width, left_eye_y, "L Outer", "green"),
        (left_eye_center_x - eye_width // 2, left_eye_y - eye_height, "L Top Outer", "green"),
        (left_eye_center_x + eye_width // 2, left_eye_y - eye_height, "L Top Inner", "green"),
        (left_eye_center_x + eye_width, left_eye_y, "L Inner", "green"),
        (left_eye_center_x + eye_width // 2, left_eye_y + eye_height, "L Btm Inner", "green"),
        (left_eye_center_x - eye_width // 2, left_eye_y + eye_height, "L Btm Outer", "green"),
    ]

    # Right eye (6 points) - Blue
    right_eye_center_x = 520
    right_eye_y = 300

    points.extend([
        (right_eye_center_x - eye_width, right_eye_y, "R Inner", "blue"),
        (right_eye_center_x - eye_width // 2, right_eye_y - eye_height, "R Top Inner", "blue"),
        (right_eye_center_x + eye_width // 2, right_eye_y - eye_height, "R Top Outer", "blue"),
        (right_eye_center_x + eye_width, right_eye_y, "R Outer", "blue"),
        (right_eye_center_x + eye_width // 2, right_eye_y + eye_height, "R Btm Outer", "blue"),
        (right_eye_center_x - eye_width // 2, right_eye_y + eye_height, "R Btm Inner", "blue"),
    ])

    def draw_eyes_guide(draw):
        """Draw detailed eye shapes."""
        center_x = width // 2
        # Draw face context
        draw.arc([50, 80, 750, 520], 0, 180, fill='#8b7355', width=3)

        # Left eye detailed shape
        left_eye_shape = [
            (left_eye_center_x - eye_width, left_eye_y),
            (left_eye_center_x - eye_width // 2, left_eye_y - eye_height),
            (left_eye_center_x + eye_width // 2, left_eye_y - eye_height),
            (left_eye_center_x + eye_width, left_eye_y),
            (left_eye_center_x + eye_width // 2, left_eye_y + eye_height),
            (left_eye_center_x - eye_width // 2, left_eye_y + eye_height),
            (left_eye_center_x - eye_width, left_eye_y),
        ]
        draw.polygon(left_eye_shape, fill='white', outline='#8b7355', width=3)
        # Pupil
        draw.ellipse([left_eye_center_x - 15, left_eye_y - 15,
                     left_eye_center_x + 15, left_eye_y + 15], fill='#4a4a4a')

        # Right eye detailed shape
        right_eye_shape = [
            (right_eye_center_x - eye_width, right_eye_y),
            (right_eye_center_x - eye_width // 2, right_eye_y - eye_height),
            (right_eye_center_x + eye_width // 2, right_eye_y - eye_height),
            (right_eye_center_x + eye_width, right_eye_y),
            (right_eye_center_x + eye_width // 2, right_eye_y + eye_height),
            (right_eye_center_x - eye_width // 2, right_eye_y + eye_height),
            (right_eye_center_x - eye_width, right_eye_y),
        ]
        draw.polygon(right_eye_shape, fill='white', outline='#8b7355', width=3)
        # Pupil
        draw.ellipse([right_eye_center_x - 15, right_eye_y - 15,
                     right_eye_center_x + 15, right_eye_y + 15], fill='#4a4a4a')

        # Eyebrows
        draw.arc([180, 220, 360, 260], 0, 180, fill='#8b7355', width=6)
        draw.arc([440, 220, 620, 260], 0, 180, fill='#8b7355', width=6)

        # Nose bridge for context
        draw.line([center_x, 340, center_x, 440], fill='#8b7355', width=2)

    output = Path(__file__).parent / "eyes.png"
    return create_reference_image(width, height, points, "Eyes (12 Points)", output, draw_eyes_guide)


def generate_nose():
    """Generate nose reference image (9 points)."""
    width, height = 600, 800
    center_x = width // 2

    # Nose bridge (4 points)
    points = [
        (center_x, 200, "Bridge Top", "purple"),
        (center_x, 300, "Bridge Mid", "purple"),
        (center_x, 400, "Bridge Low", "purple"),
        (center_x, 480, "Tip", "red"),
    ]

    # Nose bottom (5 points)
    nostril_y = 520
    nostril_spread = 50
    points.extend([
        (center_x - nostril_spread - 30, nostril_y, "Left", "green"),
        (center_x - nostril_spread // 2, nostril_y - 10, "Left Mid", "green"),
        (center_x, nostril_y - 15, "Center", "red"),
        (center_x + nostril_spread // 2, nostril_y - 10, "Right Mid", "blue"),
        (center_x + nostril_spread + 30, nostril_y, "Right", "blue"),
    ])

    def draw_nose_guide(draw):
        """Draw nose shape."""
        # Draw face outline
        draw.ellipse([50, 80, width - 50, height - 50], outline='#8b7355', width=3)

        # Nose bridge line
        draw.line([(center_x, 200), (center_x, 480)], fill='#8b7355', width=4)

        # Nose tip (small bulb)
        draw.ellipse([center_x - 25, 460, center_x + 25, 500], fill='#ffe8d6', outline='#8b7355', width=3)

        # Nostrils
        draw.ellipse([center_x - nostril_spread - 40, nostril_y - 20,
                     center_x - nostril_spread - 10, nostril_y + 10],
                     fill='#4a4a4a', outline='#8b7355', width=2)
        draw.ellipse([center_x + nostril_spread + 10, nostril_y - 20,
                     center_x + nostril_spread + 40, nostril_y + 10],
                     fill='#4a4a4a', outline='#8b7355', width=2)

        # Nose sides
        draw.line([(center_x - nostril_spread - 30, nostril_y),
                  (center_x - 30, 430)], fill='#8b7355', width=2)
        draw.line([(center_x + nostril_spread + 30, nostril_y),
                  (center_x + 30, 430)], fill='#8b7355', width=2)

        # Eyes for context
        draw.ellipse([center_x - 100, 140, center_x - 40, 170], outline='#8b7355', width=2)
        draw.ellipse([center_x + 40, 140, center_x + 100, 170], outline='#8b7355', width=2)

    output = Path(__file__).parent / "nose.png"
    return create_reference_image(width, height, points, "Nose (9 Points)", output, draw_nose_guide)


def generate_mouth():
    """Generate mouth reference image (20 points)."""
    width, height = 800, 700
    center_x = width // 2

    # Outer mouth (12 points)
    mouth_y = 350
    mouth_width = 180

    points = [
        (center_x - mouth_width, mouth_y, "L Corner", "green"),
        (center_x - mouth_width + 30, mouth_y - 25, "UL Outer", "green"),
        (center_x - mouth_width + 80, mouth_y - 35, "UL Mid", "green"),
        (center_x, mouth_y - 40, "U Center", "red"),
        (center_x + mouth_width - 80, mouth_y - 35, "UR Mid", "blue"),
        (center_x + mouth_width - 30, mouth_y - 25, "UR Outer", "blue"),
        (center_x + mouth_width, mouth_y, "R Corner", "blue"),
        (center_x + mouth_width - 30, mouth_y + 35, "LR Outer", "blue"),
        (center_x + mouth_width - 80, mouth_y + 45, "LR Mid", "blue"),
        (center_x, mouth_y + 50, "L Center", "red"),
        (center_x - mouth_width + 80, mouth_y + 45, "LL Mid", "green"),
        (center_x - mouth_width + 30, mouth_y + 35, "LL Outer", "green"),
    ]

    # Inner mouth (8 points)
    inner_width = 120
    inner_offset_y = 15
    points.extend([
        (center_x - inner_width, mouth_y, "Inner L", "darkgreen"),
        (center_x - inner_width // 2, mouth_y - inner_offset_y, "Inner UL", "darkgreen"),
        (center_x, mouth_y - inner_offset_y - 5, "Inner UC", "darkred"),
        (center_x + inner_width // 2, mouth_y - inner_offset_y, "Inner UR", "darkblue"),
        (center_x + inner_width, mouth_y, "Inner R", "darkblue"),
        (center_x + inner_width // 2, mouth_y + inner_offset_y + 10, "Inner LR", "darkblue"),
        (center_x, mouth_y + inner_offset_y + 15, "Inner LC", "darkred"),
        (center_x - inner_width // 2, mouth_y + inner_offset_y + 10, "Inner LL", "darkgreen"),
    ])

    def draw_mouth_guide(draw):
        """Draw detailed mouth/lips shape."""
        # Draw lower face
        draw.arc([100, 100, 700, 600], 0, 180, fill='#8b7355', width=3)

        # Upper lip shape (outer)
        upper_lip_outer = [
            (center_x - mouth_width, mouth_y),
            (center_x - mouth_width + 30, mouth_y - 25),
            (center_x - mouth_width + 80, mouth_y - 35),
            (center_x, mouth_y - 40),
            (center_x + mouth_width - 80, mouth_y - 35),
            (center_x + mouth_width - 30, mouth_y - 25),
            (center_x + mouth_width, mouth_y),
        ]
        draw.line(upper_lip_outer, fill='#c96a72', width=6, joint='curve')

        # Lower lip shape (outer)
        lower_lip_outer = [
            (center_x - mouth_width, mouth_y),
            (center_x - mouth_width + 30, mouth_y + 35),
            (center_x - mouth_width + 80, mouth_y + 45),
            (center_x, mouth_y + 50),
            (center_x + mouth_width - 80, mouth_y + 45),
            (center_x + mouth_width - 30, mouth_y + 35),
            (center_x + mouth_width, mouth_y),
        ]
        draw.line(lower_lip_outer, fill='#c96a72', width=6, joint='curve')

        # Inner mouth opening (darker)
        inner_mouth = [
            (center_x - inner_width, mouth_y),
            (center_x - inner_width // 2, mouth_y - inner_offset_y),
            (center_x, mouth_y - inner_offset_y - 5),
            (center_x + inner_width // 2, mouth_y - inner_offset_y),
            (center_x + inner_width, mouth_y),
            (center_x + inner_width // 2, mouth_y + inner_offset_y + 10),
            (center_x, mouth_y + inner_offset_y + 15),
            (center_x - inner_width // 2, mouth_y + inner_offset_y + 10),
            (center_x - inner_width, mouth_y),
        ]
        draw.polygon(inner_mouth, fill='#4a4a4a', outline='#2a2a2a', width=2)

        # Nose for context
        draw.line([center_x, 240, center_x, 320], fill='#8b7355', width=2)

    output = Path(__file__).parent / "mouth.png"
    return create_reference_image(width, height, points, "Mouth (20 Points)", output, draw_mouth_guide)


def generate_teeth():
    """Generate teeth reference image (2 points)."""
    width, height = 600, 700
    center_x = width // 2

    points = [
        (center_x, 280, "Upper Teeth", "blue"),
        (center_x, 420, "Lower Teeth", "red"),
    ]

    def draw_teeth_guide(draw):
        """Draw open mouth with teeth."""
        # Draw face outline
        draw.ellipse([50, 50, width - 50, height - 50], outline='#8b7355', width=3)

        # Draw open mouth outline
        mouth_opening = [
            (center_x - 120, 220),
            (center_x - 80, 180),
            (center_x, 170),
            (center_x + 80, 180),
            (center_x + 120, 220),
            (center_x + 120, 480),
            (center_x + 80, 520),
            (center_x, 530),
            (center_x - 80, 520),
            (center_x - 120, 480),
        ]
        draw.polygon(mouth_opening, fill='#4a4a4a', outline='#c96a72', width=6)

        # Upper teeth row
        draw.rectangle([center_x - 100, 210, center_x + 100, 290],
                      fill='white', outline='#8b7355', width=3)
        # Individual teeth lines
        for i in range(-4, 5):
            x = center_x + i * 25
            draw.line([(x, 210), (x, 290)], fill='#8b7355', width=1)

        # Lower teeth row
        draw.rectangle([center_x - 100, 410, center_x + 100, 490],
                      fill='white', outline='#8b7355', width=3)
        # Individual teeth lines
        for i in range(-4, 5):
            x = center_x + i * 25
            draw.line([(x, 410), (x, 490)], fill='#8b7355', width=1)

        # Nose for context
        draw.line([center_x, 80, center_x, 140], fill='#8b7355', width=2)

    output = Path(__file__).parent / "teeth.png"
    return create_reference_image(width, height, points, "Teeth (2 Points)", output, draw_teeth_guide)


def generate_tongue():
    """Generate tongue reference image (3 points)."""
    width, height = 600, 700
    center_x = width // 2

    points = [
        (center_x, 250, "Tip", "red"),
        (center_x, 380, "Center", "purple"),
        (center_x, 500, "Back", "blue"),
    ]

    def draw_tongue_guide(draw):
        """Draw extended tongue."""
        # Draw lower face
        draw.arc([50, 50, width - 50, 500], 0, 180, fill='#8b7355', width=3)

        # Draw open mouth
        mouth_opening = [
            (center_x - 100, 180),
            (center_x - 70, 150),
            (center_x, 140),
            (center_x + 70, 150),
            (center_x + 100, 180),
            (center_x + 100, 220),
            (center_x + 70, 240),
            (center_x, 245),
            (center_x - 70, 240),
            (center_x - 100, 220),
        ]
        draw.polygon(mouth_opening, fill='#4a4a4a', outline='#c96a72', width=5)

        # Draw tongue shape
        tongue_shape = [
            (center_x - 50, 500),  # Back
            (center_x - 55, 400),
            (center_x - 60, 300),
            (center_x - 40, 260),
            (center_x - 20, 240),
            (center_x, 230),  # Tip
            (center_x + 20, 240),
            (center_x + 40, 260),
            (center_x + 60, 300),
            (center_x + 55, 400),
            (center_x + 50, 500),  # Back
        ]
        draw.polygon(tongue_shape, fill='#ff6b9d', outline='#c96a72', width=3)

        # Tongue center line
        draw.line([(center_x, 250), (center_x, 500)], fill='#c96a72', width=2)

        # Nose for context
        draw.line([center_x, 70, center_x, 120], fill='#8b7355', width=2)

    output = Path(__file__).parent / "tongue.png"
    return create_reference_image(width, height, points, "Tongue (3 Points)", output, draw_tongue_guide)


def generate_ears():
    """Generate ears reference image (12 points)."""
    width, height = 900, 700

    # Left ear (6 points) - Green
    left_ear_x = 200
    ear_top_y = 180
    ear_height = 350

    points = [
        (left_ear_x, ear_top_y, "L Top", "green"),
        (left_ear_x + 40, ear_top_y + 50, "L Helix", "green"),
        (left_ear_x + 50, ear_top_y + ear_height // 2, "L Middle", "green"),
        (left_ear_x + 20, ear_top_y + ear_height - 100, "L Tragus", "green"),
        (left_ear_x + 5, ear_top_y + ear_height, "L Lobe Btm", "green"),
        (left_ear_x - 10, ear_top_y + ear_height - 30, "L Lobe Attach", "green"),
    ]

    # Right ear (6 points) - Blue
    right_ear_x = 700

    points.extend([
        (right_ear_x, ear_top_y, "R Top", "blue"),
        (right_ear_x - 40, ear_top_y + 50, "R Helix", "blue"),
        (right_ear_x - 50, ear_top_y + ear_height // 2, "R Middle", "blue"),
        (right_ear_x - 20, ear_top_y + ear_height - 100, "R Tragus", "blue"),
        (right_ear_x - 5, ear_top_y + ear_height, "R Lobe Btm", "blue"),
        (right_ear_x + 10, ear_top_y + ear_height - 30, "R Lobe Attach", "blue"),
    ])

    def draw_ears_guide(draw):
        """Draw detailed ear shapes."""
        center_x = width // 2

        # Draw head silhouettes (side view)
        # Left side head
        draw.arc([50, 100, 350, 600], 180, 360, fill='#8b7355', width=3)
        # Right side head
        draw.arc([550, 100, 850, 600], 180, 360, fill='#8b7355', width=3)

        # Left ear detailed shape
        left_ear_outline = [
            (left_ear_x, ear_top_y),  # Top
            (left_ear_x + 40, ear_top_y + 50),  # Helix
            (left_ear_x + 50, ear_top_y + ear_height // 2),  # Middle
            (left_ear_x + 40, ear_top_y + ear_height - 80),
            (left_ear_x + 5, ear_top_y + ear_height),  # Lobe bottom
            (left_ear_x - 10, ear_top_y + ear_height - 30),  # Lobe attach
            (left_ear_x - 5, ear_top_y + ear_height - 100),
            (left_ear_x, ear_top_y + ear_height // 2 + 50),
            (left_ear_x + 5, ear_top_y + 100),
            (left_ear_x, ear_top_y),
        ]
        draw.polygon(left_ear_outline, fill='#ffe8d6', outline='#8b7355', width=4)

        # Left ear inner details
        draw.arc([left_ear_x + 10, ear_top_y + 80, left_ear_x + 40, ear_top_y + 280],
                180, 270, fill='#8b7355', width=2)
        draw.ellipse([left_ear_x - 5, ear_top_y + ear_height - 60,
                     left_ear_x + 15, ear_top_y + ear_height - 20],
                     fill='#ffe8d6', outline='#8b7355', width=2)

        # Right ear detailed shape
        right_ear_outline = [
            (right_ear_x, ear_top_y),  # Top
            (right_ear_x - 40, ear_top_y + 50),  # Helix
            (right_ear_x - 50, ear_top_y + ear_height // 2),  # Middle
            (right_ear_x - 40, ear_top_y + ear_height - 80),
            (right_ear_x - 5, ear_top_y + ear_height),  # Lobe bottom
            (right_ear_x + 10, ear_top_y + ear_height - 30),  # Lobe attach
            (right_ear_x + 5, ear_top_y + ear_height - 100),
            (right_ear_x, ear_top_y + ear_height // 2 + 50),
            (right_ear_x - 5, ear_top_y + 100),
            (right_ear_x, ear_top_y),
        ]
        draw.polygon(right_ear_outline, fill='#ffe8d6', outline='#8b7355', width=4)

        # Right ear inner details
        draw.arc([right_ear_x - 40, ear_top_y + 80, right_ear_x - 10, ear_top_y + 280],
                270, 360, fill='#8b7355', width=2)
        draw.ellipse([right_ear_x - 15, ear_top_y + ear_height - 60,
                     right_ear_x + 5, ear_top_y + ear_height - 20],
                     fill='#ffe8d6', outline='#8b7355', width=2)

    output = Path(__file__).parent / "ears.png"
    return create_reference_image(width, height, points, "Ears (12 Points)", output, draw_ears_guide)


def main():
    """Generate all reference images."""
    print("Generating landmark reference images...")
    print("=" * 50)

    if not PIL_AVAILABLE:
        print("ERROR: PIL/Pillow is required to generate images.")
        print("Install with: pip install Pillow")
        return

    # Generate all images
    generators = [
        ("Face Outline", generate_face_outline),
        ("Eyebrows", generate_eyebrows),
        ("Eyes", generate_eyes),
        ("Nose", generate_nose),
        ("Mouth", generate_mouth),
        ("Teeth", generate_teeth),
        ("Tongue", generate_tongue),
        ("Ears", generate_ears),
    ]

    success_count = 0
    for name, generator in generators:
        print(f"\nGenerating {name}...")
        if generator():
            success_count += 1
        else:
            print(f"  Failed to generate {name}")

    print("\n" + "=" * 50)
    print(f"Successfully generated {success_count}/{len(generators)} images")
    print("\nImages saved to:", Path(__file__).parent)
    print("\nYou can now use these reference images in the Manual Landmark Picker!")


if __name__ == "__main__":
    main()
