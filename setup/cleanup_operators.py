'''
Cleanup and uninstall operators for Expresso addon
'''

import bpy
from bpy.types import Operator


class EXPRESSO_OT_cleanup_data(Operator):
    """Clean up Expresso data from the current scene"""
    bl_idname = "expresso.cleanup_data"
    bl_label = "Clean Up Expresso Data"
    bl_options = {'REGISTER', 'UNDO'}

    clean_objects: bpy.props.BoolProperty(
        name="Remove Expresso Objects",
        description="Remove facial_landmarks and other Expresso-specific objects",
        default=True
    )

    clean_actions: bpy.props.BoolProperty(
        name="Remove Expresso Actions",
        description="Remove actions created by Expresso (with CRIG suffix)",
        default=False
    )

    clean_collections: bpy.props.BoolProperty(
        name="Remove Expresso Collections",
        description="Remove collections created by Expresso",
        default=False
    )

    reset_preferences: bpy.props.BoolProperty(
        name="Reset Preferences",
        description="Reset Expresso addon preferences to defaults",
        default=False
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Select data to clean up:", icon='INFO')
        layout.separator()

        # Count items that would be cleaned
        obj_count = sum(1 for name in ["facial_landmarks", "2D Sliders"]
                       if context.scene.objects.get(name))

        try:
            from ..ctrl_rig.control_rig_animation_operators import CRIG_ACTION_SUFFIX
            action_count = sum(1 for action in bpy.data.actions
                             if CRIG_ACTION_SUFFIX in action.name)
        except:
            action_count = 0

        coll_count = sum(1 for name in ["2D Sliders", "Expresso_Collections"]
                        if bpy.data.collections.get(name))

        col = layout.column(align=True)
        row = col.row()
        row.prop(self, "clean_objects")
        row.label(text=f"({obj_count} found)" if obj_count else "(none found)")

        row = col.row()
        row.prop(self, "clean_actions")
        row.label(text=f"({action_count} found)" if action_count else "(none found)")

        row = col.row()
        row.prop(self, "clean_collections")
        row.label(text=f"({coll_count} found)" if coll_count else "(none found)")

        col.separator()
        col.prop(self, "reset_preferences")

        layout.separator()

        # Show helpful info
        total_items = obj_count + action_count + coll_count
        if total_items == 0:
            layout.label(text="No Expresso data found in current file", icon='INFO')
        else:
            layout.label(text=f"Total: {total_items} items can be cleaned", icon='CHECKMARK')

        layout.separator()
        layout.label(text="This operation cannot be undone!", icon='ERROR')

    def execute(self, context):
        cleaned_items = []

        # Clean Expresso objects
        if self.clean_objects:
            expresso_object_names = ["facial_landmarks", "2D Sliders"]
            for obj_name in expresso_object_names:
                obj = context.scene.objects.get(obj_name)
                if obj:
                    bpy.data.objects.remove(obj, do_unlink=True)
                    cleaned_items.append(f"Object: {obj_name}")

        # Clean Expresso actions
        if self.clean_actions:
            from ..ctrl_rig.control_rig_animation_operators import CRIG_ACTION_SUFFIX
            actions_to_remove = []
            for action in bpy.data.actions:
                if CRIG_ACTION_SUFFIX in action.name:
                    actions_to_remove.append(action)

            for action in actions_to_remove:
                bpy.data.actions.remove(action)
                cleaned_items.append(f"Action: {action.name}")

        # Clean Expresso collections
        if self.clean_collections:
            expresso_collections = ["2D Sliders", "Expresso_Collections"]
            for coll_name in expresso_collections:
                coll = bpy.data.collections.get(coll_name)
                if coll:
                    bpy.data.collections.remove(coll)
                    cleaned_items.append(f"Collection: {coll_name}")

        # Reset preferences
        if self.reset_preferences:
            prefs = context.preferences.addons.get(__package__.split('.')[0])
            if prefs:
                prefs.preferences.web_links = True
                prefs.preferences.use_vertex_size_scaling = True
                prefs.preferences.default_vertex_size = 3
                prefs.preferences.landmarks_vertex_size = 8
                prefs.preferences.auto_lock_3d_view = True
                prefs.preferences.dynamic_shape_key_ranges = True
                cleaned_items.append("Preferences reset to defaults")

        if cleaned_items:
            self.report({'INFO'}, f"Successfully cleaned {len(cleaned_items)} items")
            print(f"\nExpresso Cleanup Report ({len(cleaned_items)} items):")
            print("-" * 50)
            for item in cleaned_items:
                print(f"  ✓ {item}")
            print("-" * 50)
        else:
            # Check if nothing was selected OR nothing exists to clean
            has_checkboxes = (self.clean_objects or self.clean_actions or
                            self.clean_collections or self.reset_preferences)

            if not has_checkboxes:
                self.report({'WARNING'}, "No cleanup options selected. Please check at least one option.")
            else:
                self.report({'INFO'}, "No Expresso data found to clean in this file")

        return {'FINISHED'}


class EXPRESSO_OT_uninstall_addon(Operator):
    """Uninstall the EXPRESSO addon from Blender"""
    bl_idname = "expresso.uninstall_addon"
    bl_label = "Confirm Uninstall"
    bl_options = {'REGISTER'}

    cleanup_before_uninstall: bpy.props.BoolProperty(
        name="Clean up Expresso data before uninstalling",
        description="Remove Expresso objects, actions, and collections from the current file",
        default=True
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=450)

    def draw(self, context):
        layout = self.layout

        layout.label(text="Are you sure you want to uninstall EXPRESSO?", icon='ERROR')
        layout.separator()

        col = layout.column(align=True)
        col.label(text="This will:")
        col.label(text="  • Disable the EXPRESSO addon")
        col.label(text="  • Remove it from Blender's addon list")
        col.label(text="  • Require a Blender restart to complete")

        layout.separator()
        layout.prop(self, "cleanup_before_uninstall")

        if self.cleanup_before_uninstall:
            box = layout.box()
            col = box.column(align=True)
            col.label(text="Optional cleanup will remove:", icon='INFO')
            col.label(text="  • Expresso objects (facial_landmarks, 2D Sliders)")
            col.label(text="  • Expresso actions (with CRIG suffix)")
            col.label(text="  • Expresso collections")

        layout.separator()
        layout.label(text="You can reinstall later from the ZIP file", icon='CHECKMARK')

    def execute(self, context):
        import os
        import sys
        from pathlib import Path

        addon_module = __package__.split('.')[0]

        # Step 1: Optional cleanup
        if self.cleanup_before_uninstall:
            try:
                # Run cleanup with all options
                bpy.ops.expresso.cleanup_data(
                    clean_objects=True,
                    clean_actions=True,
                    clean_collections=True,
                    reset_preferences=False
                )
                self.report({'INFO'}, "Cleaned up Expresso data from current file")
            except Exception as e:
                self.report({'WARNING'}, f"Cleanup failed: {e}")

        # Step 2: Find addon installation path
        addon_path = None
        try:
            # Try to get path from loaded module
            for module_name, module in sys.modules.items():
                if module_name == addon_module and hasattr(module, '__file__'):
                    if module.__file__:  # Make sure __file__ is not None
                        addon_path = Path(module.__file__).parent
                        break

            # Fallback: search in standard addon locations
            if not addon_path or not addon_path.exists():
                for search_path in bpy.utils.script_paths(subdir="addons"):
                    test_path = Path(search_path) / addon_module
                    if test_path.exists():
                        addon_path = test_path
                        break
        except Exception as e:
            self.report({'WARNING'}, f"Error finding path: {e}")

        # Step 3: Save path to clipboard and file for user
        uninstall_script = None
        if addon_path and addon_path.exists():
            try:
                # Create a batch/shell script for easy deletion
                import tempfile
                script_dir = Path(tempfile.gettempdir())

                # Windows batch file
                if sys.platform == "win32":
                    script_path = script_dir / "uninstall_expresso.bat"
                    script_content = f'''@echo off
echo Expresso Addon Uninstaller
echo.
echo This will delete the Expresso addon from:
echo {addon_path}
echo.
pause
echo.
echo Deleting addon folder...
rmdir /s /q "{addon_path}"
if %ERRORLEVEL% EQU 0 (
    echo.
    echo SUCCESS! Expresso addon has been removed.
    echo Please restart Blender.
) else (
    echo.
    echo ERROR: Could not delete folder.
    echo Please manually delete: {addon_path}
)
echo.
pause
'''
                else:
                    # macOS/Linux shell script
                    script_path = script_dir / "uninstall_expresso.sh"
                    script_content = f'''#!/bin/bash
echo "Expresso Addon Uninstaller"
echo ""
echo "This will delete the Expresso addon from:"
echo "{addon_path}"
echo ""
read -p "Press Enter to continue..."
echo ""
echo "Deleting addon folder..."
rm -rf "{addon_path}"
if [ $? -eq 0 ]; then
    echo ""
    echo "SUCCESS! Expresso addon has been removed."
    echo "Please restart Blender."
else
    echo ""
    echo "ERROR: Could not delete folder."
    echo "Please manually delete: {addon_path}"
fi
echo ""
read -p "Press Enter to exit..."
'''

                # Write the script
                with open(script_path, 'w') as f:
                    f.write(script_content)

                # Make executable on Unix systems
                if sys.platform != "win32":
                    os.chmod(script_path, 0o755)

                uninstall_script = script_path

            except Exception as e:
                self.report({'WARNING'}, f"Could not create uninstall script: {e}")

        # Step 4: Disable the addon
        try:
            bpy.ops.preferences.addon_disable(module=addon_module)
            self.report({'INFO'}, "✓ EXPRESSO addon has been disabled")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to disable addon: {e}")
            return {'CANCELLED'}

        # Step 5: Show instructions to user
        if addon_path and addon_path.exists():
            self.report({'WARNING'}, "=" * 60)
            self.report({'WARNING'}, "MANUAL STEP REQUIRED:")
            self.report({'WARNING'}, "=" * 60)
            self.report({'INFO'}, "1. CLOSE BLENDER COMPLETELY")
            self.report({'INFO'}, "2. DELETE this folder:")
            self.report({'INFO'}, f"   {addon_path}")

            if uninstall_script:
                self.report({'INFO'}, "")
                self.report({'INFO'}, "EASY METHOD: Run this script after closing Blender:")
                self.report({'INFO'}, f"   {uninstall_script}")

            self.report({'INFO'}, "")
            self.report({'INFO'}, "3. RESTART BLENDER")
            self.report({'WARNING'}, "=" * 60)

            # Try to copy path to clipboard
            try:
                # Windows
                if sys.platform == "win32":
                    import subprocess
                    subprocess.run(['clip'], input=str(addon_path).encode(), check=True)
                    self.report({'INFO'}, "✓ Path copied to clipboard!")
            except:
                pass  # Clipboard copy is optional

        else:
            self.report({'ERROR'}, "Could not locate addon folder!")
            self.report({'INFO'}, "Check these locations manually:")
            for path in bpy.utils.script_paths(subdir="addons"):
                self.report({'INFO'}, f"  {path}")

        return {'FINISHED'}
