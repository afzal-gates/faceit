"""
Image reference system for manual landmark picker.
Loads and manages reference images to help users identify landmark positions.
"""

import bpy
import os
from pathlib import Path


# Map category names to image filenames
LANDMARK_REFERENCE_IMAGES = {
    "Face Outline": "face_outline.png",
    "Eyebrows": "eyebrows.png",
    "Eyes": "eyes.png",
    "Nose": "nose.png",
    "Mouth": "mouth.png",
    "Teeth": "teeth.png",
    "Tongue": "tongue.png",
    "Ears": "ears.png",
}


def get_landmark_references_path():
    """Get the path to the landmark references directory."""
    addon_dir = Path(__file__).parent.parent
    return addon_dir / "resources" / "landmark_references"


def get_reference_image_path(category_name):
    """
    Get the full path to a reference image for a category.
    Returns None if the image file doesn't exist.
    """
    filename = LANDMARK_REFERENCE_IMAGES.get(category_name)
    if not filename:
        return None

    image_path = get_landmark_references_path() / filename
    if image_path.exists():
        return str(image_path)
    return None


def load_reference_image(category_name):
    """
    Load a reference image for a category into Blender's image data.
    Returns the image datablock or None if not found.
    """
    image_path = get_reference_image_path(category_name)
    if not image_path:
        return None

    # Check if image is already loaded
    image_name = f"faceit_landmark_ref_{category_name.lower().replace(' ', '_')}"

    if image_name in bpy.data.images:
        # Reload in case file changed
        img = bpy.data.images[image_name]
        img.reload()
        return img

    # Load new image
    try:
        img = bpy.data.images.load(image_path)
        img.name = image_name
        img.use_fake_user = True  # Keep image loaded
        return img
    except:
        return None


def unload_all_reference_images():
    """Remove all loaded landmark reference images from Blender data."""
    images_to_remove = [
        img for img in bpy.data.images
        if img.name.startswith("faceit_landmark_ref_")
    ]
    for img in images_to_remove:
        bpy.data.images.remove(img)


def get_available_categories():
    """Get list of categories that have reference images available."""
    refs_path = get_landmark_references_path()
    if not refs_path.exists():
        return []

    available = []
    for category, filename in LANDMARK_REFERENCE_IMAGES.items():
        if (refs_path / filename).exists():
            available.append(category)
    return available
