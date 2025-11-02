# Reference Image Improvements

## Enhanced Visual Guides (Updated: 2025-11-01)

All reference images have been upgraded with anatomical sketches to help users better understand landmark placement context.

### What's New

**Visual Anatomy Added:**
- Realistic head/face outlines showing proper proportions
- Detailed facial feature sketches (eyes, nose, mouth, ears)
- Skin-tone coloring (#ffe8d6) for realistic appearance
- Context features to help users orient landmarks

### Image-by-Image Improvements

#### 1. Face Outline (20KB)
- Full head silhouette with proper face shape
- Eye, nose, and mouth context features
- Shows all 17 outline points on realistic face contour

#### 2. Eyebrows (15KB)
- Detailed eyebrow shapes with natural curvature
- Eye shapes below for context
- Shows proper brow arch positions
- Nose bridge for orientation

#### 3. Eyes (15KB)
- Detailed eye shapes with white sclera and dark pupils
- Eyebrow outlines for context
- Shows proper eye anatomy (corners, lids)
- Almond-shaped realistic eye contours

#### 4. Nose (18KB)
- Full nose shape with bridge, tip, and nostrils
- Visible nostril openings (dark)
- Nose sides and contours
- Eyes for facial context

#### 5. Mouth (20KB)
- Detailed lip shapes in lip color (#c96a72)
- Upper and lower lip contours
- Inner mouth opening (dark)
- Shows all 20 landmark positions on realistic lips

#### 6. Teeth (13KB)
- Open mouth showing upper and lower teeth rows
- Individual teeth drawn with separation lines
- Realistic mouth opening shape
- Shows where to place center points on each row

#### 7. Tongue (12KB)
- Extended tongue in pink (#ff6b9d)
- Tongue shape from tip to back
- Open mouth context
- Shows 3 landmark positions clearly

#### 8. Ears (18KB)
- Detailed ear anatomy on both sides
- Helix, tragus, and lobe structures
- Inner ear details
- Head silhouettes for context

### Technical Details

**Color Scheme:**
- Skin tone: `#ffe8d6`
- Outline/features: `#8b7355` (brown)
- Lips: `#c96a72` (pinkish red)
- Tongue: `#ff6b9d` (pink)
- Background: `#f0f0f0` (light gray)
- Dark areas (mouth, pupils): `#4a4a4a`

**Landmark Point Colors:**
- Red: Center/midline landmarks
- Green: Left side landmarks
- Blue: Right side landmarks
- Purple: Special landmarks (nose bridge, tongue center)

### Benefits

✅ **Easier to Understand**: Users can see landmarks in anatomical context
✅ **Better Accuracy**: Visual guides help identify correct vertex positions
✅ **Faster Setup**: Less guesswork = faster landmark placement
✅ **Professional Quality**: Realistic anatomy makes it clear what to select

### Regenerating Images

If you want to customize or regenerate the images:

```bash
python generate_reference_images.py
```

The script creates all 8 images with:
- Customizable colors
- Adjustable positions and sizes
- Modifiable fonts and labels
- Flexible image dimensions

### Notes

- Images are optimized for Blender UI display
- PNG format for best quality
- File sizes: 12-20KB (reasonable for UI elements)
- Generated with PIL/Pillow library
