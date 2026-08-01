
import bpy

from ..core.shape_key_utils import has_shape_keys
from ..__init__ import VERSION
from ..core.expresso_utils import get_expresso_armature
from . import draw_utils
from .ui import EXPRESSO_PT_Base


class EXPRESSO_PT_BaseExpressions(EXPRESSO_PT_Base):
    UI_TABS = ('EXPRESSIONS',)

    @classmethod
    def poll(cls, context):
        if not super().poll(context):
            return False
        return bool(get_expresso_armature())


class EXPRESSO_PT_Expressions(EXPRESSO_PT_BaseExpressions, bpy.types.Panel):
    '''The expressions Panel'''
    bl_label = 'Expressions'
    bl_options = set()
    bl_idname = 'EXPRESSO_PT_Expressions'
    weblink = "https://expresso-doc.readthedocs.io/en/latest/expressions/"

    @classmethod
    def poll(cls, context):
        if not super().poll(context):
            return False
        rig = get_expresso_armature()
        return rig.name in context.scene.objects

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rig = get_expresso_armature()
        shapes_baked = rig.hide_viewport is True or scene.expresso_shapes_generated
        col = layout.column(align=True)

# START ####################### VERSION 2 ONLY #######################

        if not shapes_baked and VERSION == 2:
            box = col.box()
            row = box.row()
            if scene.expresso_expression_init_expand_ui:
                icon = 'TRIA_DOWN'
            else:
                icon = 'TRIA_RIGHT'

            row.prop(scene, 'expresso_expression_init_expand_ui', text='Create',
                     icon=icon, icon_only=True, emboss=False)
            draw_utils.draw_web_link(row, link="https://expresso-doc.readthedocs.io/en/latest/create-expressions/")
            if scene.expresso_expression_init_expand_ui:
                col_above_list = box.column(align=True)
                if shapes_baked:
                    col_above_list.enabled = False
                if scene.expresso_armature_type == 'ANY':
                    # if not rig.data.expresso_control_bones:
                    #     draw_utils.draw_text_block(
                    #         col_above_list,
                    #         text="No Control Bones registered for Expresso Rig (see Setup).",
                    #         heading_icon='ERROR'
                    #     )
                    row = col_above_list.row(align=True)
                    row.operator("expresso.register_control_bones",
                                 text="Register Control Bones (Pose Mode)", icon='ADD')
                    row.operator("expresso.select_control_bones", text="", icon='RESTRICT_SELECT_OFF')
                    row.operator("expresso.clear_control_bones", text="", icon='X')
                    row = col_above_list.row(align=True)
                    row.operator("expresso.update_control_bones")
                    col_above_list.separator()
                    row = col_above_list.row(align=True)
                    # row.operator('expresso.load_empty_expressions', text='Load Empty Expressions', icon='ACTION')
                    row.operator('expresso.append_action_to_expresso_rig', text='Load Empty Expressions', icon='ACTION')
                else:
                    row = col_above_list.row(align=True)
                    row.operator('expresso.append_action_to_expresso_rig', text='Load Expresso Expressions', icon='ACTION')
                row = col_above_list.row(align=True)
                op = row.operator('expresso.append_action_to_expresso_rig',
                                  text='Load Custom Expressions', icon='IMPORT')
                op.load_custom_path = True
                row.operator('expresso.export_expressions', text='Export Custom Expressions', icon='EXPORT')
                row = col_above_list.row(align=True)
                op = row.operator('expresso.add_expression_item', text='Add Custom Expression', icon='ADD')
                op.custom_shape = True

# END ######################### VERSION 2 ONLY #######################

# START ######################### VERSION 1 ONLY #######################
        if not shapes_baked and VERSION == 1:
            row = col.row(align=True)
            # TODO: check for the rig type. Version 1 should probably only work with Rigify rigs...
            op = row.operator('expresso.append_action_to_expresso_rig',
                              text='Load ARKit Expressions', icon='ACTION')
            op.is_version_one = True
            op.load_method = 'OVERWRITE'
            op.expressions_type = 'ARKIT'

# END ######################### VERSION 1 ONLY #######################

        if shapes_baked:
            row = col.row()
            row.label(text="Return")
            row = col.row()
            row.operator('expresso.back_to_rigging', icon='BACK')
            col.separator(factor=2)
            row = col.row()
            row.template_list('EXPRESSO_UL_ExpressionsBaked', '', bpy.context.scene,
                              'expresso_expression_list', scene, 'expresso_expression_list_index')
            row = col.row(align=True)
            row.label(text='Testing')
            row = col.row(align=True)
            row.operator('expresso.test_action', icon='ACTION')
        elif 'overwrite_shape_action' in bpy.data.actions and scene.expresso_expression_list:
            col.separator()
            row = col.row()
            row.template_list('EXPRESSO_UL_Expressions', '', bpy.context.scene,
                              'expresso_expression_list', scene, 'expresso_expression_list_index')
            col_ul = row.column(align=True)

# START ####################### VERSION 2 ONLY #######################

            if VERSION == 2:

                row = col_ul.row(align=True)
                op = row.operator('expresso.add_expression_item', text='', icon='ADD')
                op.custom_shape = True

                row = col_ul.row(align=True)
                op = row.operator('expresso.remove_expression_item', text='', icon='REMOVE')
                # op.prompt = False

# END ######################### VERSION 2 ONLY #######################

            col_ul.separator()
            col_ul.row().menu('EXPRESSO_MT_ExpressionList', text='', icon='DOWNARROW_HLT')
            col_ul.separator()
            # Move the indices
            row = col_ul.row(align=True)
            op = row.operator('expresso.move_expression_item', text='', icon='TRIA_UP')
            op.direction = 'UP'
            row = col_ul.row(align=True)
            op = row.operator('expresso.move_expression_item', text='', icon='TRIA_DOWN')
            op.direction = 'DOWN'
            row = col.row()
            row.operator('expresso.force_zero_frames', icon='FILE_REFRESH')

        elif 'overwrite_shape_action' not in bpy.data.actions and scene.expresso_expression_list:
            col.separator()
            row = col.row()
            draw_utils.draw_text_block(context, row, text='The Expression Action has been deleted.')


class EXPRESSO_PT_ExpressionOptions(EXPRESSO_PT_BaseExpressions, bpy.types.Panel):
    bl_label = 'Options'
    bl_idname = 'EXPRESSO_PT_ExpressionOptions'
    bl_options = set()
    expresso_predecessor = 'EXPRESSO_PT_Expressions'
    weblink = ""

    @classmethod
    def poll(cls, context):
        if not super().poll(context):
            return False
        scene = context.scene
        rig = scene.expresso_armature
        if rig:
            if rig.hide_viewport is True or scene.expresso_shapes_generated:
                return False
        else:
            return False
        return 'overwrite_shape_action' in bpy.data.actions and scene.expresso_expression_list

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(scene, 'expresso_use_auto_mirror_x',
                 text='Auto Mirror X', icon='MOD_MIRROR')
        row = col.row(align=True)
        row.prop(scene.tool_settings, 'use_keyframe_insert_auto', icon='RADIOBUT_ON')
        col.separator()
        row = col.row(align=True)
        row.label(text='Corrective Sculpting')
        row = col.row(align=True)
        row.prop(scene, 'expresso_use_corrective_shapes', icon='SCULPTMODE_HLT')
        if scene.expresso_use_corrective_shapes:
            row = col.row(align=True)
            row.prop(scene, 'expresso_try_mirror_corrective_shapes', expand=True, icon='MOD_MIRROR')
            # row = col.row(align=True)
            row.prop(scene, 'expresso_corrective_sk_mirror_affect_only_selected_objects',
                     text='', icon='RESTRICT_SELECT_OFF')
            if scene.expresso_try_mirror_corrective_shapes:
                row = col.row(align=True)
                row.prop(scene, 'expresso_corrective_sk_mirror_method', expand=True, icon='MOD_MIRROR')
            row = col.row(align=True)
            row.label(text='Edit Mode')
            row = col.row(align=True)
            row.prop(scene, 'expresso_corrective_shape_keys_edit_mode', icon='EDITMODE_HLT', expand=True)


class EXPRESSO_UL_Expressions(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            scene = context.scene
            row = layout.row(align=True)
            row.prop(item, 'name', text='', emboss=False, icon='KEYFRAME')
            if item.mirror_name:
                op = row.operator('expresso.mirror_overwrite', text='', icon='MOD_MIRROR')
                op.expression_to_mirror = item.name
            elif scene.expresso_use_auto_mirror_x:
                row.label(text='', icon='MOD_MIRROR')
            op = row.operator('expresso.pose_amplify', text='', icon='ARROW_LEFTRIGHT')
            op.expression_index = scene.expresso_expression_list.find(item.name)
            op = row.operator('expresso.reset_expression', text='', icon='LOOP_BACK')
            op.expression_to_reset = item.name
            if scene.expresso_use_corrective_shapes:
                op = row.operator('expresso.add_corrective_shape_key_to_expression', text='', icon='SCULPTMODE_HLT')
                op.expression = item.name
                sub = row.row(align=True)
                if item.corr_shape_key:
                    op = sub.operator('expresso.remove_corrective_shape_key', text='', icon='X')
                    op.expression = item.name
                else:
                    op = sub.operator('expresso.remove_corrective_shape_key', text='',
                                      emboss=False, icon='RADIOBUT_OFF')
                    op.expression = item.name
                    sub.enabled = False


class EXPRESSO_UL_ExpressionsBaked(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(item, 'name', text='', emboss=False, icon='KEYFRAME')


class EXPRESSO_MT_ExpressionList(bpy.types.Menu):
    bl_label = 'Expression List Menu'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        row.operator('expresso.load_arkit_refernce', icon='USER')
        if VERSION == 2:
            row = layout.row()
            row.operator('expresso.clear_expresso_expressions', icon='TRASH')
        row = layout.row(align=True)
        op = row.operator('expresso.force_zero_frames', icon='FILE_REFRESH')
        row = layout.row(align=True)
        op = row.operator('expresso.cleanup_unused_fcurves', icon='FCURVE')
        row = layout.row(align=True)
        op = row.operator('expresso.reevaluate_corrective_shape_keys', icon='SHAPEKEY_DATA')
