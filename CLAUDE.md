# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Expresso is a Blender add-on (v2.3.56) for facial expressions and performance capture. It provides facial rigging, ARKit-based shape key retargeting, live motion capture (FaceCap, Epic Live Link Face, iFacialMocap, Audio2Face), and a control rig system. Licensed GPL-3.0, originally by Fynn Braren. This fork (`develop-maximo-rig` branch) adds custom features like manual landmark placement and shape key driver controls.

## Development Environment

- **Runtime**: Blender Python (bpy) — no standalone execution, no pip packages
- **Min Blender version**: 4.2.0 (manifest), but code has compat paths back to 2.80
- **Manifest**: `blender_manifest.toml` (Blender 4.2+ extension format). Note: `id` must match the package directory name
- **Legacy metadata**: `bl_info` dict in `__init__.py` for older Blender versions
- **Package directory**: Should be named `expresso/` to match the manifest `id`
- **Testing**: Manual testing inside Blender — no automated test suite. Enable addon in Edit > Preferences > Add-ons, then use the EXPRESSO panel in the 3D Viewport sidebar (N-panel)
- **Reloading**: After code changes, disable/re-enable the addon or restart Blender. For module reloads during development, `cleanse_modules()` in `__init__.py` handles cleanup

## Architecture

### Auto-loading System

`auto_load.py` (adapted from Animation Nodes by Jacques Lucke) automatically discovers and registers all Blender classes. No manual registration lists needed:

1. Recursively finds all `.py` files in subpackages
2. Collects classes inheriting from Blender base types (Panel, Operator, PropertyGroup, etc.)
3. Topologically sorts them by dependency (annotations, `bl_parent_id`, `expresso_predecessor`)
4. Calls `register()`/`unregister()` on modules that define them

**Key implication**: Adding a new operator or panel class to any `.py` file in any subpackage auto-registers it. No imports needed in `__init__.py` files.

### Module Organization

| Module | Purpose |
|---|---|
| `core/` | Shared utilities: `expresso_utils` (object/mode helpers), `expresso_data` (vertex groups, bone lists, shape data, resource paths), `arkit_shapes` (shape name mappings for ARKIT/FACECAP/EPIC/A2F), `shape_key_utils`, `mesh_utils`, `vgroup_utils`, `retarget_list_base/utils` |
| `setup/` | Object registration, vertex group assignment, cleanup/uninstall operators |
| `landmarks/` | Facial landmark placement — both auto (`landmarks_operators/utils/data`) and manual vertex picker system (`manual_landmarks_*`) |
| `rigging/` | Rig generation from landmarks using `resources/ExpressoRig.blend`, body join, pivot management |
| `bind/` | Binding (surface deform) between rig and registered face objects |
| `ctrl_rig/` | Control rig generation/baking/drivers/custom sliders using `resources/ExpressoControlRig.blend` |
| `animate/` | Expression/animation utilities for posing the rig |
| `shape_keys/` | Shape key operations: corrective shapes, driver toggles, misc operators |
| `retargeting/` | ARKit shape name retargeting and mapping lists |
| `retarget_fbx/` | FBX-based retargeting workflow |
| `mocap/` | Live mocap: OSC receiver, decoders for FaceCap/Epic Live Link/iFacialMocap, importers |
| `bake/` | Baking shape keys and modifiers from rig to mesh |
| `panels/` | All UI panels. `ui.py` defines `EXPRESSO_PT_Base`/`EXPRESSO_PT_BaseSub` base classes |
| `properties/` | Scene-level property definitions (one file per module domain), registered via `register()` functions |
| `resources/` | Blend files (rig, landmarks, control rig, reference model), expression presets, landmark reference images |

### UI Structure

The addon lives in a single sidebar tab "EXPRESSO" in the 3D Viewport. `EXPRESSO_PT_MainPanel` is the root panel with workspace/tab switching:

- **Workspaces**: ALL, RIG, MOCAP — filter which panels are visible
- **Tabs**: SETUP, SHAPES, CREATE, EXPRESSIONS, BAKE, CONTROL, MOCAP — workflow stages
- **Panel pinning**: Users can pin panels across tabs via `expresso_pin_panels`

Panels inherit from `EXPRESSO_PT_Base` and declare `UI_TABS` and `UI_WORKSPACES` tuples to control visibility.

### Naming Conventions

- **Operators**: `EXPRESSO_OT_OperatorName` with `bl_idname = 'expresso.operator_name'`
- **Panels**: `EXPRESSO_PT_PanelName` with `bl_idname = 'EXPRESSO_PT_PanelName'`
- **Properties**: Scene properties prefixed `expresso_` (e.g., `scene.expresso_face_objects`, `scene.expresso_armature`)
- **Vertex groups**: Prefixed `expresso_` (e.g., `expresso_main`, `expresso_left_eyeball`)

### Key Data Flow

1. **Setup**: User registers face mesh objects → assigns vertex groups for face regions
2. **Landmarks**: Position facial landmarks on the mesh (auto or manual vertex picker)
3. **Rigging**: Generate rig from landmarks (appends from `ExpressoRig.blend`, scales/positions bones)
4. **Binding**: Bind rig to face objects via surface deform
5. **Expressions**: Create/import ARKit expression poses on the rig
6. **Baking**: Bake rig poses to shape keys on the mesh
7. **Control Rig**: Optional control rig layer with custom sliders and drivers
8. **Mocap**: Live or recorded motion capture drives shape keys via retarget mappings

### Resource Files

`core/expresso_data.py` defines paths to blend resources. Access via helper functions:
- `get_rig_file()`, `get_landmarks_file()`, `get_control_rig_file()`, `get_arkit_reference()`
- `get_retargeting_presets()`, `get_expression_presets(rig_type)`

### Shape Key Systems

The addon supports multiple mocap engine formats with different shape name conventions. `core/arkit_shapes.py` contains the mapping dictionaries: ARKIT, FACECAP, EPIC, A2F, TONGUE, PHONEMES. Face regions in `FACE_REGIONS_BASE` (expresso_data.py) group shapes by anatomical area.

### Custom Features (this fork)

- **Manual landmarks** (`landmarks/manual_landmarks_*`): Vertex picker for placing 68-point facial landmarks by clicking mesh vertices, with reference images in `resources/landmark_references/`
- **Shape key driver toggle** (`shape_keys/shape_key_driver_toggle.py`): Toggle drivers on shape keys for manual editing control
