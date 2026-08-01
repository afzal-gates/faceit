# Manual Landmark Picker - Testing Checklist

## Pre-Testing Setup
- [ ] Blender is closed (to ensure clean addon reload)
- [ ] Addon directory is properly set
- [ ] Test scene has a character head mesh available

## 1. Addon Loading
- [ ] Start Blender
- [ ] Enable Expresso addon in preferences
- [ ] Check for any error messages in system console
- [ ] Verify addon loads without errors

## 2. UI Presence
- [ ] Open 3D View sidebar (N panel)
- [ ] Navigate to Expresso panel
- [ ] Switch to CREATE tab
- [ ] Expand "Landmarks" section
- [ ] Verify "Manual Landmark Picker" sub-panel exists
- [ ] Panel should show target mesh selector

## 3. Basic Functionality

### Initialize Landmarks
- [ ] Select a mesh object in viewport
- [ ] Set it as Target Mesh in panel
- [ ] Click "Initialize Manual Landmarks" button
- [ ] Verify landmark collection is created
- [ ] Verify statistics show "0/68" progress

### Pick Single Landmark
- [ ] Expand any category (e.g., "Eyes")
- [ ] Click "Pick" button next to a landmark
- [ ] Verify mesh switches to Edit Mode
- [ ] Select a single vertex
- [ ] Click "Pick" button again
- [ ] Verify vertex index is displayed
- [ ] Verify progress updates to "1/68"
- [ ] Verify checkmark icon appears next to landmark

### Clear Landmark
- [ ] Find a set landmark
- [ ] Click the X button next to it
- [ ] Verify landmark is cleared
- [ ] Verify progress decrements

## 4. Preview System

### Enable Preview
- [ ] Set at least 3-5 landmarks
- [ ] Enable "Preview Landmarks" toggle
- [ ] Verify empty objects appear at landmark positions
- [ ] Verify empties are labeled with landmark names
- [ ] Verify empties show in front of geometry

### Disable Preview
- [ ] Disable "Preview Landmarks" toggle
- [ ] Verify all preview empties are removed
- [ ] Verify collection "Expresso_Manual_Landmarks_Preview" is removed

## 5. Category Organization
- [ ] Verify landmarks are organized by category:
  - [ ] Face Outline (17 points)
  - [ ] Eyebrows (10 points)
  - [ ] Eyes (12 points)
  - [ ] Nose (9 points)
  - [ ] Mouth (20 points)
- [ ] Verify category statistics update correctly

## 6. Quick Landmark Setup
- [ ] Verify "Quick Landmark Setup" sub-panel appears
- [ ] Verify it shows only unset landmarks
- [ ] Pick landmarks from quick view
- [ ] Verify panel disappears when all landmarks are set

## 7. Export/Import

### Export
- [ ] Set 5-10 landmarks
- [ ] Click "Export" button
- [ ] Choose file location and name
- [ ] Verify JSON file is created
- [ ] Open JSON file and verify structure

### Import
- [ ] Clear all landmarks
- [ ] Click "Import" button
- [ ] Select previously exported JSON file
- [ ] Verify landmarks are restored
- [ ] Verify vertex indices match original

## 8. Clear All
- [ ] Set several landmarks
- [ ] Click "Clear All" button
- [ ] Confirm in dialog
- [ ] Verify all landmarks are cleared
- [ ] Verify progress shows "0/68"
- [ ] Verify preview is disabled

## 9. Data Persistence
- [ ] Set 10+ landmarks
- [ ] Enable preview
- [ ] Save .blend file
- [ ] Close Blender
- [ ] Reopen Blender and .blend file
- [ ] Verify landmarks are preserved
- [ ] Verify preview can be re-enabled
- [ ] Verify all landmark data is intact

## 10. Edge Cases

### Multiple Vertices Selected
- [ ] Try to pick landmark with multiple vertices selected
- [ ] Verify warning message appears
- [ ] Verify landmark is not set

### No Vertex Selected
- [ ] Try to confirm pick with no vertex selected
- [ ] Verify warning message appears
- [ ] Verify landmark is not set

### Invalid Target Mesh
- [ ] Try to pick with no target mesh set
- [ ] Verify appropriate warning appears

### Re-pick Existing Landmark
- [ ] Set a landmark
- [ ] Click refresh icon to re-pick
- [ ] Select different vertex
- [ ] Verify landmark updates to new vertex

### Mesh Object Deleted
- [ ] Set landmarks on a mesh
- [ ] Delete the mesh object
- [ ] Verify preview handles missing object gracefully
- [ ] Verify no crashes occur

## 11. Integration Testing

### With Existing Expresso Features
- [ ] Verify manual landmarks don't interfere with automatic landmarks
- [ ] Verify rigging operations still work
- [ ] Verify other Expresso panels still function

### Undo/Redo
- [ ] Pick a landmark
- [ ] Press Ctrl+Z (undo)
- [ ] Verify landmark is cleared
- [ ] Press Ctrl+Shift+Z (redo)
- [ ] Verify landmark is restored

## 12. Performance
- [ ] Set all 68 landmarks
- [ ] Enable preview with all landmarks
- [ ] Verify viewport performance is acceptable
- [ ] Rotate view to check framerate
- [ ] Verify no lag in UI interactions

## 13. Error Handling
- [ ] Check Blender console for any error messages
- [ ] Verify all operations fail gracefully
- [ ] Verify user gets appropriate feedback for errors

## Known Limitations (Document if found)
- Maximum number of landmarks: 68 (predefined)
- Single mesh support only (multi-mesh requires re-selection)
- Preview empties are simple spheres (no customization yet)

## Test Results Summary
**Date:** ___________
**Tester:** ___________
**Blender Version:** ___________
**Expresso Version:** ___________

**Tests Passed:** __ / __
**Tests Failed:** __ / __
**Critical Issues:** ___________
**Minor Issues:** ___________

**Overall Status:** [ ] PASS [ ] FAIL [ ] NEEDS REVISION

## Issues Found
| Issue # | Severity | Description | Steps to Reproduce | Status |
|---------|----------|-------------|-------------------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
