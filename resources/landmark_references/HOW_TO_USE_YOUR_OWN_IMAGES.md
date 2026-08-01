# How to Use Your Own Reference Images

Since I cannot access Google Image URLs or copyrighted stock photos directly, I've created a tool that lets you use **your own** reference images!

## Quick Start Guide

### Step 1: Download Reference Images

Find and download reference images of a human head. Good sources:

**Free Options:**
- Google Images (search: "3D head model", "face anatomy", "human head reference")
- Sketchfab (free 3D models - take screenshots)
- ArtStation (reference sheets)
- Pinterest (anatomy references)
- WikiMedia Commons (free images)

**What to Look For:**
- Clear, front-facing head images
- Good lighting and contrast
- Neutral expression works best
- High resolution (at least 800x800px)

### Step 2: Prepare Your Images

Save images with these **exact** filenames in the `source_images/` folder:

```
source_images/
├── face_outline_source.jpg   (or .png)
├── eyebrows_source.jpg
├── eyes_source.jpg
├── nose_source.jpg
├── mouth_source.jpg
├── teeth_source.jpg
├── tongue_source.jpg
└── ears_source.jpg
```

**Tips:**
- You can use `.jpg`, `.png`, or `.jpeg` format
- All 8 images can be the same base image (cropped differently)
- Or use specialized images for each feature (e.g., close-up of eyes for eyes_source.jpg)

### Step 3: Run the Overlay Script

```bash
cd "E:\AddOns\Customized Addons\Expresso\expresso\resources\landmark_references"
python overlay_landmarks_on_images.py
```

The script will:
1. Load your source images
2. Overlay colored landmark points
3. Add labels to each point
4. Save final reference images

### Step 4: Adjust Positions (Optional)

If landmark points don't align perfectly with your images, edit `overlay_landmarks_on_images.py`:

**Find the landmark configuration:**
```python
"face_outline": {
    "landmarks": [
        (0.50, 0.95, "0: Chin", "red"),  # x%, y%, label, color
        # x = horizontal position (0.0 = left, 1.0 = right)
        # y = vertical position (0.0 = top, 1.0 = bottom)
    ]
}
```

**Adjust positions:**
- Change `0.50` to move horizontally (0.0-1.0)
- Change `0.95` to move vertically (0.0-1.0)
- Re-run script to see changes

## Recommended Image Setup

### Option A: One Base Image for All
1. Download one good front-facing head image
2. Copy it 8 times with different names
3. Script will use the same image for all categories
4. Adjust landmark positions in script if needed

### Option B: Specialized Images per Feature
1. **face_outline_source**: Full face, front view
2. **eyebrows_source**: Close-up of eyebrow area
3. **eyes_source**: Close-up of eyes
4. **nose_source**: Close-up of nose
5. **mouth_source**: Close-up of mouth (closed or slightly open)
6. **teeth_source**: Open mouth showing teeth
7. **tongue_source**: Extended tongue
8. **ears_source**: Side view of head showing both ears (or two separate ear shots)

## Example Workflow

```bash
# 1. Create source images directory
mkdir source_images

# 2. Download a reference image (example: from your browser)
# Save as: source_images/base_head.jpg

# 3. Copy to all required names
cd source_images
copy base_head.jpg face_outline_source.jpg
copy base_head.jpg eyebrows_source.jpg
copy base_head.jpg eyes_source.jpg
copy base_head.jpg nose_source.jpg
copy base_head.jpg mouth_source.jpg
copy base_head.jpg teeth_source.jpg
copy base_head.jpg tongue_source.jpg
copy base_head.jpg ears_source.jpg

# 4. Go back and run overlay script
cd ..
python overlay_landmarks_on_images.py
```

## Troubleshooting

**"No source images found"**
- Check that images are in `source_images/` folder
- Verify filenames match exactly (including `_source.jpg`)
- Make sure images aren't corrupted

**"Landmarks are in wrong positions"**
- Edit `overlay_landmarks_on_images.py`
- Adjust the `(x_ratio, y_ratio)` values
- Values are percentages: 0.0 = start, 1.0 = end
- Re-run script after changes

**"Image quality is poor"**
- Use higher resolution source images (1000x1000px or larger)
- Use PNG instead of JPG for better quality
- Avoid heavily compressed images

## Using Stock Images You Found

If you found good images from those iStock or Adobe Stock links you shared:

### Free Alternative (Recommended):
1. Search for similar free images on:
   - Unsplash.com
   - Pexels.com
   - Pixabay.com
   - WikiMedia Commons

### If You Have Stock Account:
1. Purchase/download the image
2. Save to `source_images/` folder
3. Rename to match required filenames
4. Run the overlay script

## Result

After running the script, you'll have professional reference images with:
- ✅ Your chosen base imagery
- ✅ Colored landmark points overlaid
- ✅ Clear labels for each point
- ✅ Ready to use in Blender's Manual Landmark Picker

## Need Help?

The current generated images (with anatomical sketches) are already functional and ready to use. This custom image tool is **optional** - use it only if you want to use specific reference photos instead of the generated diagrams.
