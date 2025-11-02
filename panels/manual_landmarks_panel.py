"""
UI Panel for manual landmark picker feature.
Provides interface for setting, viewing, and managing manual facial landmarks.
"""

import bpy
from .ui import FACEIT_PT_BaseSub
from ..landmarks.manual_landmarks_data import get_landmark_label_dict, get_landmark_categories
from ..landmarks.manual_landmarks_images import load_reference_image, get_reference_image_path
from ..core import faceit_utils as futils


class FACEIT_PT_ManualLandmarks(FACEIT_PT_BaseSub, bpy.types.Panel):
    """Panel for manual landmark setup"""
    bl_label = "Manual Landmark Picker"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "FACEIT_PT_Landmarks"
    bl_idname = "FACEIT_PT_ManualLandmarks"
    faceit_predecessor = "FACEIT_PT_LandmarkHelpers"

    @classmethod
    def poll(cls, context):
        if super().poll(context):
            return True
        return False

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='OUTLINER_DATA_POINTCLOUD')

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column(align=True)

        # Target Mesh Selection
        box = col.box()
        box_col = box.column(align=True)
        box_col.label(text="Target Mesh:", icon='MESH_DATA')
        box_col.prop(scene, "faceit_manual_landmarks_target_mesh", text="")

        if not scene.faceit_manual_landmarks_target_mesh:
            box_col.label(text="Select a mesh to begin", icon='INFO')
            return

        col.separator()

        # Initialize button
        if len(scene.faceit_manual_landmarks) == 0:
            row = col.row()
            row.scale_y = 1.5
            row.operator("faceit.initialize_manual_landmarks", icon='ADD')
            return

        # Statistics
        total_landmarks = len(scene.faceit_manual_landmarks)
        set_landmarks = sum(1 for lm in scene.faceit_manual_landmarks if lm.is_set)

        box = col.box()
        box_col = box.column(align=True)
        row = box_col.row(align=True)
        row.label(text=f"Progress: {set_landmarks}/{total_landmarks}", icon='INFO')
        row = box_col.row(align=True)
        progress = set_landmarks / total_landmarks if total_landmarks > 0 else 0
        row.progress(factor=progress, type='BAR', text=f"{int(progress*100)}%")

        col.separator()

        # Options
        box = col.box()
        box_col = box.column(align=True)
        box_col.label(text="Options:", icon='PREFERENCES')
        row = box_col.row()
        row.prop(scene, "faceit_manual_landmarks_preview", text="Preview Landmarks", icon='HIDE_OFF')
        row = box_col.row()
        row.prop(scene, "faceit_manual_landmarks_mirror", text="Mirror Landmarks", icon='MOD_MIRROR')
        row = box_col.row()
        row.prop(scene, "faceit_manual_landmarks_show_reference", text="Show Reference Images", icon='IMAGE_DATA')

        box_col.separator()

        # Reset button (prominent with warning color)
        row = box_col.row()
        row.scale_y = 1.3
        row.alert = True
        row.operator("faceit.reset_manual_landmarks", text="Reset All Landmarks", icon='FILE_REFRESH')

        col.separator()

        # Category-based landmark list
        label_dict = get_landmark_label_dict()
        categories = get_landmark_categories()

        # Map category names to property names
        category_expand_props = {
            "Face Outline": "faceit_manual_landmarks_expand_face_outline",
            "Eyebrows": "faceit_manual_landmarks_expand_eyebrows",
            "Eyes": "faceit_manual_landmarks_expand_eyes",
            "Nose": "faceit_manual_landmarks_expand_nose",
            "Mouth": "faceit_manual_landmarks_expand_mouth",
            "Teeth": "faceit_manual_landmarks_expand_teeth",
            "Tongue": "faceit_manual_landmarks_expand_tongue",
            "Ears": "faceit_manual_landmarks_expand_ears",
        }

        for category_name, landmark_ids in categories.items():
            box = col.box()
            box_col = box.column(align=True)

            # Get expand property for this category
            expand_prop_name = category_expand_props.get(category_name, "")
            is_expanded = getattr(scene, expand_prop_name, True) if expand_prop_name else True

            # Category header with expand/collapse toggle
            row = box_col.row(align=True)

            # Expand/collapse icon toggle
            if expand_prop_name:
                icon = 'TRIA_DOWN' if is_expanded else 'TRIA_RIGHT'
                row.prop(scene, expand_prop_name, text="", icon=icon, icon_only=True, emboss=False)

            row.label(text=category_name)

            # Get landmarks in this category
            category_landmarks = [
                lm for lm in scene.faceit_manual_landmarks
                if lm.landmark_id in landmark_ids
            ]

            # Count set landmarks in category
            category_set = sum(1 for lm in category_landmarks if lm.is_set)
            category_total = len(category_landmarks)

            row = box_col.row()
            row.scale_y = 0.8
            row.label(text=f"{category_set}/{category_total} set")

            # Only show landmarks if expanded
            if is_expanded:
                box_col.separator(factor=0.5)

                # Show reference image if enabled and available
                if scene.faceit_manual_landmarks_show_reference:
                    ref_image = load_reference_image(category_name)
                    if ref_image:
                        # Display reference image
                        ref_box = box_col.box()
                        ref_col = ref_box.column(align=True)
                        ref_col.label(text="Reference:", icon='IMAGE_DATA')
                        ref_col.template_preview(ref_image, show_buttons=False)
                        box_col.separator(factor=0.3)

                # List all landmarks in category
                for lm in category_landmarks:
                    row = box_col.row(align=True)
                    row.scale_y = 0.9

                    # Landmark status icon
                    if lm.is_set:
                        row.label(text="", icon='CHECKMARK')
                    else:
                        row.label(text="", icon='BLANK1')

                    # Landmark label
                    landmark_label = label_dict.get(lm.landmark_id, lm.landmark_id)
                    row.label(text=landmark_label)

                    # Pick button
                    if not lm.is_set:
                        op = row.operator("faceit.pick_landmark_vertex", text="Pick", icon='EYEDROPPER')
                        op.landmark_id = lm.landmark_id
                    else:
                        # Show vertex index
                        row.label(text=f"V:{lm.vertex_index}")
                        # Re-pick button
                        op = row.operator("faceit.pick_landmark_vertex", text="", icon='FILE_REFRESH')
                        op.landmark_id = lm.landmark_id
                        # Clear button
                        op = row.operator("faceit.clear_landmark", text="", icon='X')
                        op.landmark_id = lm.landmark_id

            box_col.separator(factor=0.3)

        col.separator()

        # Rig Generation
        box = col.box()
        box_col = box.column(align=True)
        box_col.label(text="Rig Generation:", icon='ARMATURE_DATA')

        # Show validation status
        set_count = sum(1 for lm in scene.faceit_manual_landmarks if lm.is_set)
        total_count = len(scene.faceit_manual_landmarks)

        # Status message
        if set_count < 30:
            row = box_col.row()
            row.label(text=f"Need at least 30 landmarks ({set_count}/85)", icon='ERROR')
        elif set_count < total_count * 0.7:
            row = box_col.row()
            row.label(text=f"Partial coverage ({set_count}/85)", icon='INFO')
        else:
            row = box_col.row()
            row.label(text=f"Ready ({set_count}/85)", icon='CHECKMARK')

        # Generate rig button
        row = box_col.row()
        row.scale_y = 1.5
        op = row.operator("faceit.generate_rig_from_manual_landmarks", text="Generate Rig", icon='ARMATURE_DATA')
        row.enabled = set_count >= 30

        col.separator()

        # Actions
        box = col.box()
        box_col = box.column(align=True)
        box_col.label(text="Data Management:", icon='MODIFIER')

        row = box_col.row(align=True)
        row.operator("faceit.export_manual_landmarks", text="Export", icon='EXPORT')
        row.operator("faceit.import_manual_landmarks", text="Import", icon='IMPORT')


class FACEIT_PT_ManualLandmarksQuickView(FACEIT_PT_BaseSub, bpy.types.Panel):
    """Simplified panel showing only unset landmarks"""
    bl_label = "Quick Landmark Setup"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "FACEIT_PT_ManualLandmarks"
    bl_idname = "FACEIT_PT_ManualLandmarksQuickView"

    @classmethod
    def poll(cls, context):
        if super().poll(context):
            scene = context.scene
            if len(scene.faceit_manual_landmarks) > 0:
                # Only show if there are unset landmarks
                return any(not lm.is_set for lm in scene.faceit_manual_landmarks)
        return False

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column(align=True)
        col.label(text="Unset Landmarks:", icon='INFO')

        label_dict = get_landmark_label_dict()

        unset_landmarks = [lm for lm in scene.faceit_manual_landmarks if not lm.is_set]

        if len(unset_landmarks) == 0:
            col.label(text="All landmarks set!", icon='CHECKMARK')
            return

        # Show up to 10 unset landmarks
        for i, lm in enumerate(unset_landmarks[:10]):
            row = col.row(align=True)
            landmark_label = label_dict.get(lm.landmark_id, lm.landmark_id)
            op = row.operator("faceit.pick_landmark_vertex", text=landmark_label, icon='EYEDROPPER')
            op.landmark_id = lm.landmark_id

        if len(unset_landmarks) > 10:
            col.label(text=f"... and {len(unset_landmarks) - 10} more")
