"""
Operators for toggling shape key drivers to enable manual control.
When drivers are active, they override manual shape key values.
This module provides operators to mute/unmute drivers for manual editing.
"""

import bpy
from bpy.types import Operator
from bpy.props import BoolProperty

from ..core import faceit_utils as futils
from ..core import shape_key_utils as sk_utils


class FACEIT_OT_ToggleShapeKeyDrivers(Operator):
    """Toggle (mute/unmute) all shape key drivers to enable manual control"""
    bl_idname = "faceit.toggle_shape_key_drivers"
    bl_label = "Toggle Shape Key Drivers"
    bl_options = {'REGISTER', 'UNDO'}

    mute: BoolProperty(
        name="Mute Drivers",
        description="Mute all shape key drivers to enable manual control",
        default=True
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        faceit_objects = futils.get_faceit_objects_list()
        if not faceit_objects:
            self.report({'WARNING'}, "No FaceIt objects found")
            return {'CANCELLED'}

        total_drivers = 0
        affected_objects = 0

        for obj in faceit_objects:
            if not sk_utils.has_shape_keys(obj):
                continue

            shapekeys = obj.data.shape_keys
            if not shapekeys or not shapekeys.animation_data:
                continue

            drivers = shapekeys.animation_data.drivers
            if not drivers:
                continue

            obj_driver_count = 0
            for dr in drivers:
                if 'key_blocks' in dr.data_path and '.value' in dr.data_path:
                    dr.mute = self.mute
                    obj_driver_count += 1

            if obj_driver_count > 0:
                total_drivers += obj_driver_count
                affected_objects += 1

        if total_drivers == 0:
            self.report({'INFO'}, "No shape key drivers found")
            return {'FINISHED'}

        status = "muted" if self.mute else "unmuted"
        self.report(
            {'INFO'},
            f"{status.capitalize()} {total_drivers} driver(s) on {affected_objects} object(s)"
        )

        # Force viewport update
        context.scene.frame_set(context.scene.frame_current)

        return {'FINISHED'}


class FACEIT_OT_MuteShapeKeyDrivers(Operator):
    """Mute all shape key drivers to enable manual shape key control"""
    bl_idname = "faceit.mute_shape_key_drivers"
    bl_label = "Enable Manual Control"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.faceit.toggle_shape_key_drivers('EXEC_DEFAULT', mute=True)
        return {'FINISHED'}


class FACEIT_OT_UnmuteShapeKeyDrivers(Operator):
    """Unmute all shape key drivers to restore automatic control"""
    bl_idname = "faceit.unmute_shape_key_drivers"
    bl_label = "Enable Driver Control"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.faceit.toggle_shape_key_drivers('EXEC_DEFAULT', mute=False)
        return {'FINISHED'}


class FACEIT_OT_RemoveSpecificShapeKeyDriver(Operator):
    """Remove driver from a specific shape key to allow permanent manual control"""
    bl_idname = "faceit.remove_shape_key_driver"
    bl_label = "Remove Driver"
    bl_options = {'REGISTER', 'UNDO'}

    shape_key_name: bpy.props.StringProperty(
        name="Shape Key Name",
        description="Name of the shape key to remove driver from"
    )

    object_name: bpy.props.StringProperty(
        name="Object Name",
        description="Name of the object containing the shape key"
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if not self.object_name or not self.shape_key_name:
            self.report({'WARNING'}, "Object name and shape key name required")
            return {'CANCELLED'}

        obj = bpy.data.objects.get(self.object_name)
        if not obj:
            self.report({'WARNING'}, f"Object '{self.object_name}' not found")
            return {'CANCELLED'}

        if not sk_utils.has_shape_keys(obj):
            self.report({'WARNING'}, f"Object '{self.object_name}' has no shape keys")
            return {'CANCELLED'}

        shapekeys = obj.data.shape_keys
        if not shapekeys.animation_data:
            self.report({'INFO'}, "No drivers found on this object")
            return {'FINISHED'}

        # Find and remove the driver
        dp = f'key_blocks["{self.shape_key_name}"].value'
        dr = shapekeys.animation_data.drivers.find(dp)

        if dr:
            shapekeys.animation_data.drivers.remove(dr)
            # Reset the shape key value
            if self.shape_key_name in shapekeys.key_blocks:
                shapekeys.key_blocks[self.shape_key_name].value = 0.0
            self.report({'INFO'}, f"Removed driver from '{self.shape_key_name}'")
        else:
            self.report({'INFO'}, f"No driver found for '{self.shape_key_name}'")

        # Force viewport update
        context.scene.frame_set(context.scene.frame_current)

        return {'FINISHED'}


class FACEIT_OT_ListShapeKeyDrivers(Operator):
    """List all shape keys with drivers in the console"""
    bl_idname = "faceit.list_shape_key_drivers"
    bl_label = "List Shape Key Drivers"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        faceit_objects = futils.get_faceit_objects_list()
        if not faceit_objects:
            self.report({'WARNING'}, "No FaceIt objects found")
            return {'CANCELLED'}

        print("\n" + "="*60)
        print("SHAPE KEY DRIVERS REPORT")
        print("="*60 + "\n")

        total_drivers = 0
        for obj in faceit_objects:
            if not sk_utils.has_shape_keys(obj):
                continue

            shapekeys = obj.data.shape_keys
            if not shapekeys or not shapekeys.animation_data:
                continue

            drivers = shapekeys.animation_data.drivers
            if not drivers:
                continue

            obj_drivers = []
            for dr in drivers:
                if 'key_blocks' in dr.data_path and '.value' in dr.data_path:
                    # Extract shape key name from data path
                    import re
                    match = re.search(r'key_blocks\["(.+?)"\]', dr.data_path)
                    if match:
                        sk_name = match.group(1)
                        mute_status = "MUTED" if dr.mute else "ACTIVE"
                        obj_drivers.append(f"  - {sk_name} [{mute_status}]")

            if obj_drivers:
                print(f"Object: {obj.name}")
                print("\n".join(obj_drivers))
                print()
                total_drivers += len(obj_drivers)

        print("="*60)
        print(f"Total drivers found: {total_drivers}")
        print("="*60 + "\n")

        self.report({'INFO'}, f"Found {total_drivers} shape key drivers (see console for details)")

        return {'FINISHED'}
