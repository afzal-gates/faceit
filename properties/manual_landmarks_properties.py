"""
Properties for manual landmark picker feature.
Stores landmark data including vertex indices and object references.
"""

import bpy
from bpy.props import (
    IntProperty,
    StringProperty,
    BoolProperty,
    CollectionProperty,
    EnumProperty,
    PointerProperty
)
from bpy.types import PropertyGroup, Scene, Object


class ManualLandmarkItem(PropertyGroup):
    """Stores data for a single manual landmark point."""

    landmark_id: StringProperty(
        name="Landmark ID",
        description="Unique identifier for this landmark",
        default=""
    )

    vertex_index: IntProperty(
        name="Vertex Index",
        description="Index of the selected vertex on the mesh",
        default=-1
    )

    object_name: StringProperty(
        name="Object Name",
        description="Name of the mesh object containing this landmark vertex",
        default=""
    )

    is_set: BoolProperty(
        name="Is Set",
        description="Whether this landmark has been assigned",
        default=False
    )


def update_preview_landmarks(self, context):
    """Update handler for preview toggle."""
    # Check if operator is available to avoid registration order issues
    if not hasattr(bpy.ops.faceit, 'preview_manual_landmarks'):
        return

    if self.faceit_manual_landmarks_preview:
        # Enable preview - will be handled by operator
        try:
            bpy.ops.faceit.preview_manual_landmarks('INVOKE_DEFAULT', enable=True)
        except:
            pass
    else:
        # Disable preview
        try:
            bpy.ops.faceit.preview_manual_landmarks('INVOKE_DEFAULT', enable=False)
        except:
            pass


def register():
    # ManualLandmarkItem is auto-registered by auto_load.py
    # Only register Scene properties here

    Scene.faceit_manual_landmarks = CollectionProperty(
        name="Manual Landmarks",
        type=ManualLandmarkItem,
        description="Collection of manually placed facial landmarks"
    )

    Scene.faceit_manual_landmarks_preview = BoolProperty(
        name="Preview Landmarks",
        description="Display empties at landmark positions for visualization",
        default=False,
        update=update_preview_landmarks
    )

    Scene.faceit_manual_landmarks_active = IntProperty(
        name="Active Landmark",
        description="Currently selected landmark index",
        default=0
    )

    Scene.faceit_landmark_picker_active = BoolProperty(
        name="Landmark Picker Active",
        description="Whether the landmark picker is currently running",
        default=False
    )

    Scene.faceit_manual_landmarks_target_mesh = PointerProperty(
        name="Target Mesh",
        description="The mesh object to pick landmarks from",
        type=Object,
        poll=lambda self, obj: obj.type == 'MESH'
    )

    # Mirror option
    Scene.faceit_manual_landmarks_mirror = BoolProperty(
        name="Mirror Landmarks",
        description="Automatically set mirrored landmarks (left/right) when picking vertices",
        default=False
    )

    # Show reference images option
    Scene.faceit_manual_landmarks_show_reference = BoolProperty(
        name="Show Reference Images",
        description="Display reference images to help identify landmark positions",
        default=True
    )

    # Expand/collapse properties for categories
    Scene.faceit_manual_landmarks_expand_face_outline = BoolProperty(
        name="Expand Face Outline",
        description="Show/hide Face Outline landmarks",
        default=True
    )

    Scene.faceit_manual_landmarks_expand_eyebrows = BoolProperty(
        name="Expand Eyebrows",
        description="Show/hide Eyebrows landmarks",
        default=True
    )

    Scene.faceit_manual_landmarks_expand_eyes = BoolProperty(
        name="Expand Eyes",
        description="Show/hide Eyes landmarks",
        default=True
    )

    Scene.faceit_manual_landmarks_expand_nose = BoolProperty(
        name="Expand Nose",
        description="Show/hide Nose landmarks",
        default=True
    )

    Scene.faceit_manual_landmarks_expand_mouth = BoolProperty(
        name="Expand Mouth",
        description="Show/hide Mouth landmarks",
        default=True
    )

    Scene.faceit_manual_landmarks_expand_teeth = BoolProperty(
        name="Expand Teeth",
        description="Show/hide Teeth landmarks",
        default=True
    )

    Scene.faceit_manual_landmarks_expand_tongue = BoolProperty(
        name="Expand Tongue",
        description="Show/hide Tongue landmarks",
        default=True
    )

    Scene.faceit_manual_landmarks_expand_ears = BoolProperty(
        name="Expand Ears",
        description="Show/hide Ears landmarks",
        default=True
    )


def unregister():
    del Scene.faceit_manual_landmarks_expand_ears
    del Scene.faceit_manual_landmarks_expand_tongue
    del Scene.faceit_manual_landmarks_expand_teeth
    del Scene.faceit_manual_landmarks_expand_mouth
    del Scene.faceit_manual_landmarks_expand_nose
    del Scene.faceit_manual_landmarks_expand_eyes
    del Scene.faceit_manual_landmarks_expand_eyebrows
    del Scene.faceit_manual_landmarks_expand_face_outline
    del Scene.faceit_manual_landmarks_show_reference
    del Scene.faceit_manual_landmarks_mirror
    del Scene.faceit_manual_landmarks_target_mesh
    del Scene.faceit_landmark_picker_active
    del Scene.faceit_manual_landmarks_active
    del Scene.faceit_manual_landmarks_preview
    del Scene.faceit_manual_landmarks

    # ManualLandmarkItem is auto-unregistered by auto_load.py
