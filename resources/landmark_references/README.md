# Landmark Reference Images

This directory contains reference images for the Manual Landmark Picker to help users identify which vertices to select for each landmark.

## Image Requirements

### File Format
- **Format:** PNG (recommended) or JPG
- **Color:** RGB or RGBA
- **Dimensions:** Recommended 512x512 to 1024x1024 pixels
- **Quality:** High resolution for clarity when zoomed

### Naming Convention

Images must be named exactly as follows:

| Category | Filename |
|----------|----------|
| Face Outline | `face_outline.png` |
| Eyebrows | `eyebrows.png` |
| Eyes | `eyes.png` |
| Nose | `nose.png` |
| Mouth | `mouth.png` |
| Teeth | `teeth.png` |
| Tongue | `tongue.png` |
| Ears | `ears.png` |

## Image Content Guidelines

### What to Include in Each Image

Each reference image should clearly show:

1. **Labeled Landmark Points**
   - Mark each landmark position with a colored dot or marker
   - Use different colors for left/right symmetry (e.g., red for left, blue for right)
   - Label each point with its landmark name or number

2. **Clear Annotations**
   - Add arrows or lines pointing to specific features
   - Include brief text descriptions if needed
   - Use contrasting colors for visibility

3. **Multiple Views (Optional)**
   - Consider showing front, side, or 3/4 views if helpful
   - Use split-screen layouts for multiple angles

### Example Content for Each Category

**Face Outline** (17 points)
- Show the full face perimeter
- Mark all 17 points from chin center around to the other side
- Indicate direction/numbering clearly

**Eyebrows** (10 points total)
- Show both eyebrows
- Mark inner, inner-mid, center, outer-mid, outer points for each side
- Distinguish left vs right

**Eyes** (12 points total)
- Show both eyes with 6 points each
- Mark outer corner, top outer, top inner, inner corner, bottom inner, bottom outer
- Show natural eye shape

**Nose** (9 points)
- Show bridge (top, mid, low), tip
- Show nostril area (left, left-mid, center, right-mid, right)
- Front view works best

**Mouth** (20 points)
- Show outer lip contour (12 points)
- Show inner mouth opening (8 points)
- Mark corners, cupid's bow, center points
- Consider showing both closed and slightly open mouth

**Teeth** (2 points)
- Show upper and lower teeth center points
- Best shown with mouth slightly open
- Mark approximate center of upper and lower teeth rows

**Tongue** (3 points)
- Show tongue extended
- Mark tip, center, and back positions
- Side view may be helpful for back position

**Ears** (12 points total, 6 per ear)
- Show both ears (or create separate images)
- Mark top, helix, middle, tragus, lobe bottom, lobe attachment
- Side/profile view works best

## Creating Reference Images

### Recommended Tools

- **Image Editing:** Photoshop, GIMP, Krita
- **3D Screenshots:** Blender viewport with annotations
- **Drawing:** Inkscape, Illustrator for vector graphics

### Tips for Creating Clear References

1. **Use High Contrast**
   - Dark markers on light backgrounds or vice versa
   - Ensure text is readable at small sizes

2. **Consistent Style**
   - Use the same color scheme across all images
   - Keep marker size and font consistent

3. **Clear Labels**
   - Use readable fonts (sans-serif recommended)
   - Size text appropriately for the image resolution

4. **Test Visibility**
   - View at actual size in Blender's UI
   - Ensure all markers are distinguishable

## Using Reference Images

Once images are placed in this directory with the correct filenames:

1. Open the Manual Landmark Picker panel
2. Enable "Show Reference Images" option
3. Expand any category
4. Reference image will appear at the top of the landmark list

## Example Workflow

1. Take a screenshot of a reference model in Blender
2. Open in image editor
3. Add colored dots for each landmark position
4. Add text labels
5. Save as PNG with appropriate filename
6. Place in this directory
7. Restart Blender or reload addon

## Troubleshooting

**Image not showing:**
- Check filename matches exactly (case-sensitive)
- Verify image is in PNG or JPG format
- Ensure file is not corrupted
- Check "Show Reference Images" is enabled

**Image quality issues:**
- Increase source image resolution
- Use PNG format for better quality
- Avoid JPEG compression artifacts

**Image too large/small:**
- Blender will auto-scale, but 512-1024px is optimal
- Maintain square aspect ratio for best results
