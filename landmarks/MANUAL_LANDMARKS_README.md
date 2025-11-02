# Manual Landmark Picker Feature

## Overview
The Manual Landmark Picker allows users to manually assign facial landmark points by selecting vertices on the mesh. This provides more control than automatic landmark detection and is useful for characters with non-standard topology.

## Usage Instructions

### 1. Initial Setup
1. Navigate to the **FaceIt** panel in the 3D View sidebar (N panel)
2. Go to the **CREATE** tab
3. Expand the **Landmarks** section
4. Find the **Manual Landmark Picker** sub-panel

### 2. Select Target Mesh
1. In the **Target Mesh** field, select the mesh object you want to pick landmarks from
2. This should typically be your main face mesh

### 3. Initialize Landmarks
1. Click the **Initialize Manual Landmarks** button
2. This creates entries for all 68 standard facial landmark points

### 4. Pick Landmark Points
For each landmark:
1. Click the **Pick** button next to the landmark label
2. The addon will switch to Edit Mode on your target mesh
3. Select a single vertex that represents that landmark point
4. Click the **Pick** button again to confirm the selection
5. The vertex index will be stored and displayed

**Tips:**
- Use the **Quick Landmark Setup** sub-panel to see only unset landmarks
- Landmarks are organized by category (Face Outline, Eyebrows, Eyes, Nose, Mouth)
- You can re-pick a landmark by clicking the refresh icon
- Clear individual landmarks with the X button

### 5. Preview Landmarks
1. Enable **Preview Landmarks** toggle
2. Empty objects will appear at each set landmark position
3. Empties are labeled with the landmark name
4. Disable preview to hide the empties

### 6. Export/Import
**Export:**
1. Click **Export** button
2. Choose a file location and name (JSON format)
3. All set landmarks will be saved

**Import:**
1. Click **Import** button
2. Select a previously exported JSON file
3. Landmarks will be loaded and applied

### 7. Clear Landmarks
- **Individual:** Click X button next to any landmark
- **All:** Click **Clear All** button (requires confirmation)

## Landmark Point Definitions

### Face Outline (17 points)
- face_outline_0 to face_outline_16
- Traces the jaw line from chin to temples

### Eyebrows (10 points)
- Left: left_eyebrow_outer, outer_mid, center, inner_mid, inner
- Right: right_eyebrow_inner, inner_mid, center, outer_mid, outer

### Eyes (12 points)
- 6 points per eye tracing the eye socket
- Includes outer, top outer, top inner, inner, bottom inner, bottom outer

### Nose (9 points)
- Bridge: 4 points from top to tip
- Bottom: 5 points across nostril base

### Mouth (20 points)
- Outer: 12 points tracing outer lip line
- Inner: 8 points tracing inner mouth opening

## Data Storage
- Landmarks are stored in the scene properties
- Data persists when saving the .blend file
- Each landmark stores: identifier, vertex index, object name, set status

## Technical Details

### Files Added
- `landmarks/manual_landmarks_data.py` - Landmark definitions
- `landmarks/manual_landmarks_operators.py` - Operators for picking/managing
- `properties/manual_landmarks_properties.py` - Property definitions
- `panels/manual_landmarks_panel.py` - UI panels

### Properties
- `Scene.faceit_manual_landmarks` - Collection of landmark data
- `Scene.faceit_manual_landmarks_preview` - Preview toggle
- `Scene.faceit_manual_landmarks_target_mesh` - Target mesh reference

### Operators
- `faceit.pick_landmark_vertex` - Pick vertex for landmark
- `faceit.clear_landmark` - Clear single landmark
- `faceit.clear_all_landmarks` - Clear all landmarks
- `faceit.initialize_manual_landmarks` - Initialize landmark collection
- `faceit.preview_manual_landmarks` - Toggle preview empties
- `faceit.export_manual_landmarks` - Export to JSON
- `faceit.import_manual_landmarks` - Import from JSON

## Integration with FaceIt
The manual landmarks are stored separately from the automatic landmarks system. They can be used:
- As reference points for custom rigging
- For verification of automatic landmark placement
- For characters where automatic detection fails
- As input for custom facial tracking or expression systems

## Future Enhancements
Potential improvements:
- Symmetry tools (mirror left/right)
- Batch operations
- Visualization options (colors, sizes)
- Integration with automatic landmark system
- Validation tools
- Template presets for common face types
