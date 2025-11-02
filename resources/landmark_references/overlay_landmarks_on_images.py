"""
Overlay landmark points on your own reference images.
Place your reference images in 'source_images/' folder and run this script.
"""

import os
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL/Pillow not available. Please install: pip install Pillow")


# Landmark configurations - adjust these positions based on your images
LANDMARK_CONFIGS = {
    "face_outline": {
        "source": "face_outline_source.jpg",  # Your image filename
        "output": "face_outline.png",
        "landmarks": [
            # Format: (x_ratio, y_ratio, label, color)
            # x_ratio and y_ratio are 0.0-1.0 (percentage of image width/height)
            (0.50, 0.95, "0: Chin", "red"),
            (0.52, 0.90, "1", "blue"),
            (0.55, 0.85, "2", "blue"),
            (0.58, 0.78, "3", "blue"),
            (0.62, 0.70, "4", "blue"),
            (0.65, 0.60, "5", "blue"),
            (0.68, 0.48, "6", "blue"),
            (0.70, 0.35, "7", "blue"),
            (0.70, 0.25, "8", "blue"),
            (0.30, 0.25, "16", "green"),
            (0.30, 0.35, "15", "green"),
            (0.32, 0.48, "14", "green"),
            (0.35, 0.60, "13", "green"),
            (0.38, 0.70, "12", "green"),
            (0.42, 0.78, "11", "green"),
            (0.45, 0.85, "10", "green"),
            (0.48, 0.90, "9", "green"),
        ]
    },
    "eyebrows": {
        "source": "eyebrows_source.jpg",
        "output": "eyebrows.png",
        "landmarks": [
            # Left eyebrow
            (0.25, 0.40, "L Outer", "green"),
            (0.30, 0.38, "L Outer Mid", "green"),
            (0.35, 0.37, "L Center", "green"),
            (0.40, 0.38, "L Inner Mid", "green"),
            (0.45, 0.40, "L Inner", "green"),
            # Right eyebrow
            (0.55, 0.40, "R Inner", "blue"),
            (0.60, 0.38, "R Inner Mid", "blue"),
            (0.65, 0.37, "R Center", "blue"),
            (0.70, 0.38, "R Outer Mid", "blue"),
            (0.75, 0.40, "R Outer", "blue"),
        ]
    },
    "eyes": {
        "source": "eyes_source.jpg",
        "output": "eyes.png",
        "landmarks": [
            # Left eye
            (0.25, 0.50, "L Outer", "green"),
            (0.30, 0.45, "L Top Outer", "green"),
            (0.40, 0.45, "L Top Inner", "green"),
            (0.45, 0.50, "L Inner", "green"),
            (0.40, 0.55, "L Btm Inner", "green"),
            (0.30, 0.55, "L Btm Outer", "green"),
            # Right eye
            (0.55, 0.50, "R Inner", "blue"),
            (0.60, 0.45, "R Top Inner", "blue"),
            (0.70, 0.45, "R Top Outer", "blue"),
            (0.75, 0.50, "R Outer", "blue"),
            (0.70, 0.55, "R Btm Outer", "blue"),
            (0.60, 0.55, "R Btm Inner", "blue"),
        ]
    },
    "nose": {
        "source": "nose_source.jpg",
        "output": "nose.png",
        "landmarks": [
            (0.50, 0.25, "Bridge Top", "purple"),
            (0.50, 0.38, "Bridge Mid", "purple"),
            (0.50, 0.50, "Bridge Low", "purple"),
            (0.50, 0.60, "Tip", "red"),
            (0.35, 0.65, "Left", "green"),
            (0.42, 0.63, "Left Mid", "green"),
            (0.50, 0.62, "Center", "red"),
            (0.58, 0.63, "Right Mid", "blue"),
            (0.65, 0.65, "Right", "blue"),
        ]
    },
    "mouth": {
        "source": "mouth_source.jpg",
        "output": "mouth.png",
        "landmarks": [
            # Outer mouth
            (0.25, 0.50, "L Corner", "green"),
            (0.30, 0.47, "UL Outer", "green"),
            (0.40, 0.45, "UL Mid", "green"),
            (0.50, 0.44, "U Center", "red"),
            (0.60, 0.45, "UR Mid", "blue"),
            (0.70, 0.47, "UR Outer", "blue"),
            (0.75, 0.50, "R Corner", "blue"),
            (0.70, 0.55, "LR Outer", "blue"),
            (0.60, 0.57, "LR Mid", "blue"),
            (0.50, 0.58, "L Center", "red"),
            (0.40, 0.57, "LL Mid", "green"),
            (0.30, 0.55, "LL Outer", "green"),
            # Inner mouth
            (0.35, 0.50, "Inner L", "darkgreen"),
            (0.42, 0.48, "Inner UL", "darkgreen"),
            (0.50, 0.47, "Inner UC", "darkred"),
            (0.58, 0.48, "Inner UR", "darkblue"),
            (0.65, 0.50, "Inner R", "darkblue"),
            (0.58, 0.53, "Inner LR", "darkblue"),
            (0.50, 0.54, "Inner LC", "darkred"),
            (0.42, 0.53, "Inner LL", "darkgreen"),
        ]
    },
    "teeth": {
        "source": "teeth_source.jpg",
        "output": "teeth.png",
        "landmarks": [
            (0.50, 0.40, "Upper Teeth", "blue"),
            (0.50, 0.60, "Lower Teeth", "red"),
        ]
    },
    "tongue": {
        "source": "tongue_source.jpg",
        "output": "tongue.png",
        "landmarks": [
            (0.50, 0.35, "Tip", "red"),
            (0.50, 0.54, "Center", "purple"),
            (0.50, 0.71, "Back", "blue"),
        ]
    },
    "ears": {
        "source": "ears_source.jpg",
        "output": "ears.png",
        "landmarks": [
            # Left ear
            (0.25, 0.30, "L Top", "green"),
            (0.27, 0.38, "L Helix", "green"),
            (0.28, 0.55, "L Middle", "green"),
            (0.26, 0.68, "L Tragus", "green"),
            (0.25, 0.80, "L Lobe Btm", "green"),
            (0.24, 0.75, "L Lobe Attach", "green"),
            # Right ear
            (0.75, 0.30, "R Top", "blue"),
            (0.73, 0.38, "R Helix", "blue"),
            (0.72, 0.55, "R Middle", "blue"),
            (0.74, 0.68, "R Tragus", "blue"),
            (0.75, 0.80, "R Lobe Btm", "blue"),
            (0.76, 0.75, "R Lobe Attach", "blue"),
        ]
    }
}


def overlay_landmarks_on_image(source_path, output_path, landmarks, title):
    """
    Overlay landmark points on a source image.

    Args:
        source_path: Path to source image
        output_path: Path to save output
        landmarks: List of (x_ratio, y_ratio, label, color) tuples
        title: Title to display
    """
    if not PIL_AVAILABLE:
        return False

    if not source_path.exists():
        print(f"  Source image not found: {source_path}")
        return False

    # Load source image
    try:
        img = Image.open(source_path)
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
    except Exception as e:
        print(f"  Error loading image: {e}")
        return False

    width, height = img.size
    draw = ImageDraw.Draw(img)

    # Try to load font
    try:
        font_title = ImageFont.truetype("arial.ttf", int(height * 0.04))
        font_label = ImageFont.truetype("arial.ttf", int(height * 0.02))
    except:
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()

    # Draw semi-transparent overlay for title area
    title_height = int(height * 0.08)
    draw.rectangle([0, 0, width, title_height], fill=(240, 240, 240, 200))

    # Draw title
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, title_height // 4), title, fill='black', font=font_title)

    # Draw landmarks
    point_size = int(min(width, height) * 0.012)  # Adaptive point size

    for x_ratio, y_ratio, label, color in landmarks:
        x = int(x_ratio * width)
        y = int(y_ratio * height)

        # Draw point with white outline for visibility
        outline_size = point_size + 3
        draw.ellipse([x - outline_size, y - outline_size, x + outline_size, y + outline_size],
                    fill='white', outline='black', width=2)
        draw.ellipse([x - point_size, y - point_size, x + point_size, y + point_size],
                    fill=color, outline='black', width=2)

        # Draw label with background
        label_bbox = draw.textbbox((0, 0), label, font=font_label)
        label_width = label_bbox[2] - label_bbox[0]
        label_height = label_bbox[3] - label_bbox[1]

        # Position label to avoid overlap (right side of point)
        label_x = x + point_size + 8
        label_y = y - label_height // 2

        # Draw label background
        padding = 3
        draw.rectangle([label_x - padding, label_y - padding,
                       label_x + label_width + padding, label_y + label_height + padding],
                      fill='white', outline='black', width=1)

        # Draw label text
        draw.text((label_x, label_y), label, fill='black', font=font_label)

    # Save output
    img.save(output_path)
    print(f"  Created: {output_path}")
    return True


def main():
    """Process all configured landmark images."""
    print("Overlay Landmark Points on Your Images")
    print("=" * 60)

    if not PIL_AVAILABLE:
        print("ERROR: PIL/Pillow is required.")
        print("Install with: pip install Pillow")
        return

    script_dir = Path(__file__).parent
    source_dir = script_dir / "source_images"

    # Create source_images directory if it doesn't exist
    if not source_dir.exists():
        source_dir.mkdir()
        print(f"\nCreated directory: {source_dir}")
        print("\nPLEASE DO THE FOLLOWING:")
        print("-" * 60)
        print("1. Download reference images of a human head/face")
        print("2. Place them in the 'source_images/' folder with these names:")
        print()
        for config in LANDMARK_CONFIGS.values():
            print(f"   - {config['source']}")
        print()
        print("3. Run this script again")
        print()
        print("TIP: Search for '3D head model' or 'face anatomy' images")
        print("     Good sources: Google Images, Sketchfab screenshots, etc.")
        print("-" * 60)
        return

    # Check which source images exist
    available = []
    missing = []

    for name, config in LANDMARK_CONFIGS.items():
        source_path = source_dir / config["source"]
        if source_path.exists():
            available.append((name, config, source_path))
        else:
            missing.append(config["source"])

    if missing:
        print("\nMissing source images:")
        for filename in missing:
            print(f"  - {filename}")
        print()
        print(f"Place your images in: {source_dir}")
        print()

    if not available:
        print("No source images found. Cannot generate reference images.")
        return

    # Process available images
    print(f"\nProcessing {len(available)} image(s)...")
    print()

    success_count = 0
    for name, config, source_path in available:
        print(f"Processing {name}...")

        output_path = script_dir / config["output"]
        title = f"{name.replace('_', ' ').title()} ({len(config['landmarks'])} Points)"

        if overlay_landmarks_on_image(source_path, output_path, config["landmarks"], title):
            success_count += 1

    print()
    print("=" * 60)
    print(f"Successfully processed {success_count}/{len(available)} images")

    if success_count > 0:
        print(f"\nReference images saved to: {script_dir}")
        print("\nYou can now use these in the Manual Landmark Picker!")

    if missing:
        print(f"\n{len(missing)} image(s) still missing. Add them to generate all references.")


if __name__ == "__main__":
    main()
