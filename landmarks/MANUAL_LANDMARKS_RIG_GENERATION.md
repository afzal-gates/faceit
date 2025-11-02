# Manual Landmarks Rig Generation

Generate facial rigs directly from manually placed landmarks in the FaceIt addon.

## Overview

The Manual Landmarks Rig Generation feature allows you to create a complete FaceIt facial rig using landmarks that you manually place on your character's mesh. This is useful when:

- Automatic landmark detection doesn't work well for your character
- You have a stylized or non-human character
- You want precise control over landmark placement
- Your character's proportions are unusual

## How It Works

The system converts your manually placed landmarks into FaceIt's standard landmark format, then uses the existing FaceIt rig generation pipeline to create a fully functional facial rig.

### Landmark Mapping

Manual landmarks (85 points) are mapped to FaceIt's internal landmark system:

- **Face Outline** → Jaw and face contour bones
- **Eyebrows** → Eyebrow deformation bones
- **Eyes** → Eyelid control bones
- **Nose** → Nose deformation bones
- **Mouth** → Lip and mouth bones
- **Teeth** → Upper and lower teeth bones
- **Tongue** → Tongue control bones
- **Ears** → Ear deformation bones

## Requirements

### Minimum Landmark Count

You need **at least 30 landmarks** placed to generate a rig. The system validates:

- **Critical landmarks** must be set:
  - Face outline (chin center and top corners)
  - Eyes (inner and outer corners for both eyes)
  - Mouth (corners and center points)
  - Nose (tip and bridge top)

### Recommended Coverage

For best results:
- **50-60 landmarks** (60-70% coverage): Basic functional rig
- **60-75 landmarks** (70-85% coverage): Good quality rig
- **75+ landmarks** (85%+ coverage): Excellent quality rig

The UI shows real-time status:
- 🔴 **Need at least 30 landmarks** - Not enough data
- 🔵 **Partial coverage (X/85)** - Can generate, but incomplete
- ✅ **Ready (X/85)** - Good coverage for rig generation

## Usage Steps

### 1. Place Manual Landmarks

1. Open **FaceIt Panel** → **Landmarks** → **Manual Landmark Picker**
2. Select your character's head mesh as **Target Mesh**
3. Click **Initialize Manual Landmarks**
4. Place landmarks by:
   - Clicking **Pick** button next to each landmark
   - Selecting a vertex in edit mode
   - Clicking operator again to confirm

**Tips:**
- Use **Mirror Landmarks** option to automatically set left/right pairs
- Enable **Preview Landmarks** to see placed points as 3D empties
- Use **Show Reference Images** to see which vertex to select
- Focus on critical landmarks first (face outline, eyes, mouth, nose)

### 2. Validate Landmark Placement

Check the **Rig Generation** section:
- Status message shows how many landmarks are set
- **Generate Rig** button becomes active at 30+ landmarks
- Review the landmark count and coverage percentage

### 3. Generate the Rig

1. Ensure your target mesh is registered in FaceIt (Setup tab)
2. Click **Generate Rig** button
3. If coverage is low (<50%), confirm the action
4. The system will:
   - Validate your landmarks
   - Create a `facial_landmarks` object
   - Call FaceIt's rig generation system
   - Generate bones and weights

### 4. Post-Generation

After rig generation:
- The facial rig armature is created
- Bones are positioned based on your landmarks
- Vertex weights are calculated automatically
- You can proceed with FaceIt's standard workflow:
  - Shape key creation
  - Control rig generation
  - Animation and expressions

## Troubleshooting

### "Insufficient landmarks set"

**Problem:** Less than 30 landmarks placed

**Solution:** Place more landmarks, especially from critical groups:
- Face outline (at least 3 points)
- Eyes (at least 4 points - both inner and outer corners)
- Mouth (at least 4 points - both corners, upper and lower center)
- Nose (at least 2 points - tip and bridge)

### "Missing critical landmark groups"

**Problem:** Entire landmark categories are missing

**Solution:** Place at least one landmark from each missing category shown in the error message.

### "Failed to create landmarks object"

**Problem:** Manual landmarks couldn't be converted to FaceIt format

**Solutions:**
- Check that all landmarks reference valid mesh objects
- Verify vertex indices are within mesh bounds
- Ensure target mesh still exists and hasn't been modified
- Try resetting and re-placing problematic landmarks

### "FaceIt rig generation operator not found"

**Problem:** FaceIt rig system isn't available

**Solutions:**
- Verify FaceIt addon is properly installed and enabled
- Restart Blender to refresh the addon
- Check FaceIt addon version compatibility
- Reinstall FaceIt if necessary

### Rig generation fails or produces poor results

**Solutions:**
- Increase landmark coverage (aim for 70%+)
- Review landmark placement accuracy:
  - Face outline should follow jaw contour
  - Eye landmarks should be at actual eye corners
  - Mouth landmarks should be on lip edges
- Check symmetry - use mirror option for balanced results
- Ensure target mesh has good topology (no ngons, good edge flow)

## Best Practices

### Landmark Placement Strategy

1. **Start with face outline** - Establishes overall proportions
2. **Add eyes and mouth** - Most critical for expressions
3. **Place nose landmarks** - Important for facial structure
4. **Add eyebrows** - Improves expression range
5. **Finish with teeth, tongue, ears** - Optional but complete

### Accuracy Tips

- **Zoom in** when selecting vertices for precise placement
- **Use orthographic view** (Numpad 1, 3, 7) for better alignment
- **Enable X-ray** mode to see through mesh
- **Select vertices on edges** rather than flat surfaces
- **Place eye landmarks** at actual eye opening, not eyeball
- **Mouth corners** should be at the crease where lips meet
- **Chin center** should be at the lowest point of jaw

### Mirror Landmarks

- Enable **Mirror Landmarks** option before placing
- Place landmarks on one side first
- System automatically finds corresponding mirrored vertex
- Review auto-mirrored positions and adjust if needed
- Center landmarks (nose, mouth center) don't mirror

### Performance Considerations

- **Complete placement** before generating rig (avoid multiple generations)
- **Save your .blend file** before rig generation
- **Export landmarks** after placement for reuse on similar characters
- **Test with 50-60 landmarks** first, then refine

## Data Management

### Export Landmarks

Save your landmark data for reuse:
1. Click **Export** in Data Management section
2. Choose location and filename (`.json`)
3. File contains vertex indices and object names

**Use cases:**
- Backup before rig generation
- Transfer to similar characters
- Share with team members
- Version control for character variants

### Import Landmarks

Load previously saved landmarks:
1. Click **Import** in Data Management section
2. Select your `.json` file
3. Landmarks are loaded and validated
4. Review placement before generating rig

**Note:** Import requires the same mesh or compatible topology.

## Technical Details

### Landmark Conversion

The system maps 85 manual landmarks to FaceIt's 72-point + special points system:

| Manual Landmarks | FaceIt System | Bone Regions |
|-----------------|---------------|--------------|
| Face Outline (17) | Indices 0-16 | Jaw, chin, temples |
| Eyebrows (10) | Indices 47-64 | Brow deformation |
| Eyes (12) | Indices 28-46, 101, 111 | Eyelids, eye centers |
| Nose (9) | Indices 14, 17-18, 21, 26-27, 36, 103-105 | Nose bridge, wings, tip |
| Mouth (20) | Indices 6-13 | Lips, mouth corners |
| Teeth (2) | Indices 106-107 | Upper/lower teeth |
| Tongue (3) | Indices 108, 112-114 | Tongue control |
| Ears (12) | Index 116 | Ear deformation |

### Special Landmarks

The system calculates derived landmarks:
- **Eye centers (101, 111)** - Average of 6 eye landmarks each
- **Jaw master (102)** - Offset from chin center
- **Face center (109)** - Average of key face points
- **Tongue master (108)** - Average of tongue landmarks

### Coordinate System

- Landmarks are stored in **world space**
- Vertex positions are transformed by mesh world matrix
- Generated `facial_landmarks` object uses world coordinates
- Rig bones are positioned at landmark locations

## Workflow Integration

### With FaceIt Standard Workflow

1. **Setup Tab**
   - Register your character mesh
   - Generate rig from manual landmarks

2. **Shape Keys Tab**
   - Create facial expressions
   - Link to rig bones

3. **Control Rig Tab**
   - Generate UI controls
   - Set up advanced features

4. **Animation Tab**
   - Create animations
   - Use control rig sliders

### With Custom Pipelines

The generated rig is a standard FaceIt rig:
- Compatible with all FaceIt features
- Exports to standard formats (FBX, glTF)
- Works with motion capture data
- Integrates with game engines

## Limitations

### Current Limitations

1. **Topology dependency** - Landmarks reference specific vertices
   - Modifying mesh topology invalidates landmarks
   - Subdividing mesh changes vertex indices
   - Use non-destructive modifiers when possible

2. **Symmetry assumptions** - Mirror function assumes X-axis symmetry
   - Characters must have left/right symmetry
   - Non-symmetric faces may need manual landmark placement

3. **Single mesh target** - All landmarks must be on one mesh
   - Teeth, tongue must be part of main head mesh
   - Separate meshes not supported (yet)

4. **Ear support limited** - FaceIt has basic ear rigging
   - All 12 ear landmarks map to general ear region
   - Detailed ear deformation may require custom bones

### Known Issues

- **Import validation** - Imported landmarks may not match modified mesh
- **Preview empties** - Many empties (85) may clutter viewport
- **Undo limitations** - Landmark placement undos work per-landmark, not batch

## Future Enhancements

Planned improvements:
- Multi-mesh support (separate teeth, tongue objects)
- Enhanced ear rigging with detailed bone structure
- Landmark auto-placement from similar characters
- Symmetry tools for asymmetric faces
- Batch processing for multiple characters
- Machine learning-assisted landmark suggestions

## Support

For issues or questions:
- Check FaceIt documentation: https://faceit-doc.readthedocs.io/
- Review this guide's troubleshooting section
- Ensure manual landmarks are properly placed
- Verify FaceIt addon is up to date
- Test with simplified character first

## Credits

Manual Landmarks Rig Generation is an extension to the FaceIt addon by Fynn Braren.
