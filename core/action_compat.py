import bpy
from bpy_extras import anim_utils as extra_anim_utils


class ActionFCurvesWrapper:
    """
    Compatibility wrapper providing an fcurves interface on Action objects
    for Blender 4.4 / 5.0+ (Animation 2025 layered/slotted action system).
    """

    def __init__(self, action):
        self._action = action

    def _all_fcurves(self):
        fcs = []
        for layer in getattr(self._action, 'layers', []):
            for strip in getattr(layer, 'strips', []):
                for cb in getattr(strip, 'channelbags', []):
                    fcs.extend(cb.fcurves)
        return fcs

    def __iter__(self):
        return iter(self._all_fcurves())

    def __len__(self):
        return len(self._all_fcurves())

    def __bool__(self):
        for layer in getattr(self._action, 'layers', []):
            for strip in getattr(layer, 'strips', []):
                for cb in getattr(strip, 'channelbags', []):
                    if len(cb.fcurves) > 0:
                        return True
        return False

    def __getitem__(self, index):
        return self._all_fcurves()[index]

    def find(self, data_path='', index=0, **kwargs):
        dp = kwargs.get('data_path', data_path)
        idx = kwargs.get('index', index)
        for layer in getattr(self._action, 'layers', []):
            for strip in getattr(layer, 'strips', []):
                for cb in getattr(strip, 'channelbags', []):
                    fc = cb.fcurves.find(dp, index=idx)
                    if fc:
                        return fc
        return None

    def new(self, data_path='', index=0, action_group='', group_name='', **kwargs):
        dp = kwargs.get('data_path', data_path)
        idx = kwargs.get('index', index)
        grp = group_name or action_group or kwargs.get('group_name', '') or kwargs.get('action_group', '')

        # 1. If assigned to an object's animation_data, use fcurve_ensure_for_datablock
        for obj in bpy.data.objects:
            if obj.animation_data and obj.animation_data.action == self._action:
                try:
                    return self._action.fcurve_ensure_for_datablock(
                        datablock=obj, data_path=dp, index=idx, group_name=grp
                    )
                except Exception:
                    pass

        # Check shape keys
        for mesh in bpy.data.meshes:
            if mesh.shape_keys and mesh.shape_keys.animation_data and mesh.shape_keys.animation_data.action == self._action:
                try:
                    return self._action.fcurve_ensure_for_datablock(
                        datablock=mesh.shape_keys, data_path=dp, index=idx, group_name=grp
                    )
                except Exception:
                    pass

        # 2. Standalone action: ensure slot and channelbag
        slot = None
        if getattr(self._action, 'slots', None):
            slot = self._action.slots[0]
        elif hasattr(self._action, 'slots'):
            slot = self._action.slots.new(id_type='OBJECT', name=self._action.name)

        cb = None
        if slot:
            if hasattr(extra_anim_utils, 'action_ensure_channelbag_for_slot'):
                cb = extra_anim_utils.action_ensure_channelbag_for_slot(self._action, slot)
            elif hasattr(extra_anim_utils, '_ensure_channelbag_exists'):
                cb = extra_anim_utils._ensure_channelbag_exists(self._action, slot)
            elif hasattr(extra_anim_utils, 'action_get_channelbag_for_slot'):
                cb = extra_anim_utils.action_get_channelbag_for_slot(self._action, slot)

        if cb is not None:
            fc = cb.fcurves.find(dp, index=idx)
            if fc:
                return fc
            try:
                return cb.fcurves.new(data_path=dp, index=idx, group_name=grp)
            except TypeError:
                return cb.fcurves.new(data_path=dp, index=idx)

        return None

    def remove(self, fcurve):
        for layer in getattr(self._action, 'layers', []):
            for strip in getattr(layer, 'strips', []):
                for cb in getattr(strip, 'channelbags', []):
                    try:
                        cb.fcurves.remove(fcurve)
                        return
                    except Exception:
                        pass


def _bone_get_select(self):
    obj = bpy.context.active_object
    if obj and obj.type == 'ARMATURE':
        pb = obj.pose.bones.get(self.name)
        if pb:
            return pb.select
    return False


def _bone_set_select(self, value):
    obj = bpy.context.active_object
    if obj and obj.type == 'ARMATURE':
        pb = obj.pose.bones.get(self.name)
        if pb:
            pb.select = bool(value)


def init_action_compatibility():
    """Ensure Action.fcurves and Bone.select are available across all Blender versions."""
    if not hasattr(bpy.types.Action, 'fcurves'):
        bpy.types.Action.fcurves = property(lambda self: ActionFCurvesWrapper(self))
    if not hasattr(bpy.types.Bone, 'select'):
        bpy.types.Bone.select = property(_bone_get_select, _bone_set_select)


# Auto-initialize when imported
init_action_compatibility()
