# Vertex Picker Feature for Landmarks

## Overview
A new feature has been added to make manual landmark adjustment much easier. Instead of manually dragging landmark vertices in 3D space, you can now simply click on vertices from your original mesh to snap landmarks to those positions.

## How to Use

### Step-by-Step Workflow

1. **Generate Landmarks** (as usual)
   - Click "Generate Landmarks" in the Landmarks panel
   - Follow the normal alignment process:
     - Align to chin position
     - Match face height
     - Match face width

2. **Project Landmarks** (as usual)
   - Click "Project Landmarks" to project the landmarks onto your face mesh
   - The landmarks object enters edit mode

3. **Use the New Vertex Picker** (NEW!)
   - You should see a new box in the panel labeled "Snap to Vertex"
   - Select one or more landmark vertices that you want to reposition
   - Click the "Pick Vertex to Snap" button (eyedropper icon)
   - Click on any vertex from your original face mesh
   - The selected landmark(s) will instantly snap to that position!

## Usage Tips

### Selecting Multiple Landmarks
- You can select multiple landmark vertices before clicking the picker
- All selected landmarks will snap to the same clicked vertex
- This is useful for grouping landmarks that should be at the same location

### Canceling the Picker
- Press **ESC** or **Right Mouse** to cancel vertex picking
- You can then select different landmark vertices and try again

### Workflow Advantages
- **Faster**: No need to manually drag vertices in 3D space
- **More Accurate**: Snaps directly to mesh vertex positions
- **Easier**: Just click where you want the landmark to be
- **Visual**: See your original mesh and click directly on it

## Technical Details

### What Happens Behind the Scenes
1. When you click the picker button, the operator enters modal mode
2. You click on your face mesh in the 3D viewport
3. A ray cast detects which face you clicked on
4. The closest vertex to your click position is found
5. The selected landmark vertices are moved to that vertex's world position
6. The position is properly transformed to the landmarks object's local space

### Requirements
- Must be in Edit Mode on the 'facial_landmarks' object
- Must have at least one landmark vertex selected
- The main face object must be accessible (assigned in Setup tab)

## Troubleshooting

### "No vertex found at clicked location"
- Try clicking closer to the actual mesh surface
- Make sure your face mesh is visible and not hidden
- Try clicking on a different area of the mesh

### "No main face object found"
- Make sure you've assigned the main vertex group in the Setup tab
- The face mesh must be properly registered with Expresso

### Button not visible
- Make sure you're in Edit Mode on the landmarks object
- The button only appears when the landmarks are in state 5 (after projection)
- Make sure you've completed the projection step first

## Comparison to Manual Landmarks Picker

This feature is different from the "Manual Landmarks Picker" system:
- **Manual Landmarks Picker**: Build landmarks from scratch by picking vertices for each named landmark point
- **Vertex Picker (this feature)**: Quick adjustment tool for the traditional landmarks workflow

Both systems have their uses:
- Use **Manual Landmarks Picker** if you want complete control from the start
- Use **Vertex Picker** if you prefer the traditional alignment workflow but want faster fine-tuning
