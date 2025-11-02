# Shape Key Driver Control Feature

## Problem

When playing shape key animations, everything works fine. However, when trying to manually change shape key values (like `jawOpen`, `tongueOut`, etc.), some shape keys don't respond to manual input.

## Root Cause

**Drivers Override Manual Input**

Shape keys controlled by the FaceIt Control Rig have **drivers** attached to them. These drivers automatically calculate shape key values based on control rig bone positions/rotations.

When you manually try to change a shape key value:
1. You move the slider
2. The driver immediately evaluates
3. The driver overrides your manual input
4. The shape key snaps back to the driver's calculated value

## Solution

This feature provides operators to **mute/unmute drivers** temporarily, allowing full manual control of shape keys when needed.

## Features

### 1. Enable Manual Control
**Operator**: `faceit.mute_shape_key_drivers`

Mutes all shape key drivers on FaceIt objects, allowing you to:
- Manually adjust any shape key value
- Test shape key combinations
- Create custom expressions without driver interference
- Sculpt or adjust shape key deformations

### 2. Enable Driver Control
**Operator**: `faceit.unmute_shape_key_drivers`

Unmutes all shape key drivers, restoring automatic control:
- Control rig bones control shape keys again
- Animation playback works normally
- Drivers calculate shape key values automatically

### 3. List Shape Key Drivers
**Operator**: `faceit.list_shape_key_drivers`

Prints a detailed report to the console showing:
- All objects with shape key drivers
- Which shape keys have drivers
- Driver mute status (ACTIVE or MUTED)

## How to Use

### Method 1: UI Panel (Recommended)

1. Go to the **SHAPES** tab in FaceIt
2. Find the **"Shape Key Driver Control"** panel
3. Click **"Enable Manual"** to mute drivers
4. Manually adjust shape keys as needed
5. Click **"Enable Drivers"** to restore automatic control

### Method 2: Search Menu

Press `F3` and search for:
- "Enable Manual Control" - Mutes drivers
- "Enable Driver Control" - Unmutes drivers
- "List Shape Key Drivers" - Shows driver info

## Use Cases

### Sculpting Shape Keys
```
1. Enable Manual Control
2. Set shape key to desired value
3. Enter Edit Mode
4. Sculpt the shape key
5. Exit Edit Mode
6. Enable Driver Control (when done)
```

### Testing Shape Combinations
```
1. Enable Manual Control
2. Manually adjust multiple shape keys
3. Test different combinations
4. Screenshot or note good combinations
5. Enable Driver Control
```

### Creating Custom Expressions
```
1. Enable Manual Control
2. Mix multiple shape keys manually
3. Create new expression from combination
4. Enable Driver Control
```

### Animation Without Control Rig
```
1. Enable Manual Control
2. Manually keyframe shape key values
3. Animate without control rig interference
4. Enable Driver Control (to restore rig control)
```

## Technical Details

### What Happens When You Mute Drivers

```python
# For each driver on shape keys:
driver.mute = True  # Driver stops evaluating
```

- Drivers are **muted**, not deleted
- All driver data is preserved
- Shape keys can be controlled manually
- Animation data remains intact

### What Happens When You Unmute Drivers

```python
# For each driver on shape keys:
driver.mute = False  # Driver resumes evaluating
```

- Drivers resume automatic calculation
- Control rig regains control
- Manual values are overridden
- Scene is refreshed to update values

### Driver Detection

The operators find drivers by searching for data paths matching:
```
key_blocks["shape_key_name"].value
```

Only shape key value drivers are affected. Other drivers (transforms, materials, etc.) are not touched.

## Troubleshooting

### Shape Keys Still Don't Respond

**Possible causes:**
1. **Action/Animation Override**: The shape key might be controlled by an Action instead of a driver
   - **Solution**: Check if there's an active Action on the shape keys
   - Remove or mute the Action in the Dope Sheet

2. **Control Rig Still Active**: The control rig might be connected
   - **Solution**: Check CONTROL tab for connection status
   - Disconnect the control rig if needed

3. **Shape Key is Locked**: The shape key itself might be locked
   - **Solution**: Check the shape key properties panel
   - Unlock the shape key

### Drivers Don't Work After Unmuting

**Possible cause:**
- Scene needs refresh

**Solution:**
```
1. Click "Enable Driver Control" button again
2. Change the timeline frame
3. Or: Press Ctrl+Z (undo) then Ctrl+Shift+Z (redo)
```

### Want to Permanently Remove Drivers

If you want to permanently remove drivers (not just mute):
1. Use the existing operator: `faceit.remove_control_drivers`
2. This is in the CONTROL tab
3. Or: Manually delete drivers in the Drivers Editor

## Best Practices

### Always Re-enable Drivers

After manual shape key work:
1. **Always** click "Enable Driver Control" to restore drivers
2. **Verify** that control rig works correctly
3. **Test** animation playback

### Don't Save with Muted Drivers

Before saving your file:
1. Click "Enable Driver Control"
2. Make sure drivers are active
3. Otherwise, the file will open with non-functional drivers

### Use for Temporary Edits Only

This feature is designed for **temporary** manual control:
- Short editing sessions
- Testing and experimentation
- Quick adjustments

For **permanent** changes:
- Edit the shape keys themselves
- Adjust control rig amplify values
- Or remove drivers completely

## Console Output Example

Clicking "List Shape Key Drivers in Console" outputs:

```
============================================================
SHAPE KEY DRIVERS REPORT
============================================================

Object: Body
  - browInnerUp [ACTIVE]
  - browDown_L [ACTIVE]
  - browDown_R [ACTIVE]
  - jawOpen [MUTED]
  - tongueOut [MUTED]

Object: Eyes
  - eyeBlink_L [ACTIVE]
  - eyeBlink_R [ACTIVE]

============================================================
Total drivers found: 7
============================================================
```

## Related Features

- **Control Rig Connection**: Connect/disconnect control rig (CONTROL tab)
- **Remove Drivers**: Permanently remove drivers (CONTROL tab)
- **Reset Expression Values**: Reset all shape keys to 0 (SHAPES tab)

## File Organization

- **Operators**: `shape_keys/shape_key_driver_toggle.py`
- **UI Panel**: `panels/shapes_panel.py`
- **Documentation**: `shape_keys/DRIVER_CONTROL_FEATURE.md`
