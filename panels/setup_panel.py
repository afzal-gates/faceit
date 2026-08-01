
import bpy
from bpy.props import StringProperty

from ..core import expresso_utils as futils
from ..core import vgroup_utils as vg_utils
from .ui import EXPRESSO_PT_Base


class EXPRESSO_PT_BaseSetup(EXPRESSO_PT_Base):
    UI_TABS = ('SETUP',)


class EXPRESSO_PT_SetupRegister(EXPRESSO_PT_BaseSetup, bpy.types.Panel):
    bl_label = 'Register Objects'
    bl_idname = 'EXPRESSO_PT_SetupRegister'
    bl_options = set()
    weblink = "https://expresso-doc.readthedocs.io/en/latest/setup/#register-geometry"

    @classmethod
    def poll(cls, context):
        return super().poll(context)

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column(align=True)

        # row = col.row(align=True)
        # row.label(text='Registration')

        # draw_utils.draw_web_link(row, 'https://expresso-doc.readthedocs.io/en/latest/setup/')

        if not scene.expresso_face_objects:
            row = col.row(align=True)
            op = row.operator('expresso.add_facial_part', text='Register Face Objects', icon='ADD')
            op.facial_part = 'main'
        else:
            col.separator(factor=1.0)
            row = col.row()
            row.template_list('FACE_OBJECTS_UL_list', '', scene, 'expresso_face_objects', scene, 'expresso_face_index')
            col_ul = row.column(align=True)
            # row.prop(scene, 'expresso_show_warnings', text='', icon='ERROR')
            row = col_ul.row(align=True)
            op = row.operator('expresso.add_facial_part', text='', icon='ADD')
            row = col_ul.row(align=True)
            op = row.operator('expresso.remove_facial_part', text='', icon='REMOVE')
            op.prompt = False
            col_ul.separator()
            row = col_ul.row()
            row.menu('EXPRESSO_MT_ExpressoObjects', text='', icon='DOWNARROW_HLT')
            col_ul.separator()
            row = col_ul.row(align=True)
            op = row.operator('expresso.move_face_object', text='', icon='TRIA_UP')
            op.direction = 'UP'
            row = col_ul.row(align=True)
            op = row.operator('expresso.move_face_object', text='', icon='TRIA_DOWN')
            op.direction = 'DOWN'
            row = col.row(align=True)
            op = row.operator('expresso.add_facial_part', icon='ADD')
            row = col.row(align=True)
            if scene.expresso_workspace.workspace != 'MOCAP' and not scene.expresso_use_existing_armature:
                row = col.row(align=True)
                op = row.operator('expresso.face_object_warning_check', text='Check Geometry', icon='CHECKMARK')
                op.item_name = 'ALL'
                op.set_show_warnings = True
                op.check_main = True
                icon_hide = 'HIDE_OFF' if scene.expresso_show_warnings else 'HIDE_ON'
                row.prop(scene, 'expresso_show_warnings', icon=icon_hide)
            row = col.row(align=True)
            row.label(text="Existing Rig")
            row = col.row(align=True)
            row.prop(scene, "expresso_body_armature", text="", icon='ARMATURE_DATA')
            if scene.expresso_use_existing_armature:  # or scene.expresso_eye_pivot_options == 'COPY_PIVOT'
                row.enabled = False
            if scene.expresso_body_armature:
                row = col.row(align=True)
                row.prop(scene.expresso_body_armature.data, "pose_position", expand=True)
                if scene.expresso_workspace.workspace != 'MOCAP':
                    col.separator()
                    row = col.row(align=True)
                    row.prop(scene, 'expresso_use_existing_armature', icon='ARMATURE_DATA')
                    if scene.expresso_use_existing_armature:
                        row = col.row(align=True)
                        row.operator("expresso.register_control_bones",
                                     text="Register Control Bones (Pose Mode)", icon='ADD')
                        row.operator("expresso.select_control_bones", text="", icon='RESTRICT_SELECT_OFF')
                        row.operator("expresso.clear_control_bones", text="", icon='X')


class EXPRESSO_PT_SetupVertexGroups(EXPRESSO_PT_BaseSetup, bpy.types.Panel):
    bl_label = 'Assign Vertex Groups'
    bl_idname = 'EXPRESSO_PT_SetupVertexGroups'
    bl_options = set()
    expresso_predecessor = 'EXPRESSO_PT_SetupRegister'
    UI_WORKSPACES = ('ALL', 'RIG')
    weblink = "https://expresso-doc.readthedocs.io/en/latest/setup/#assign-vertex-groups"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expresso_predecessor = 'EXPRESSO_PT_SetupRegister'
        self.mask_modifiers = {}
        self.assigned_vertex_groups = []

    @classmethod
    def poll(cls, context):
        if super().poll(context):
            if context.scene.expresso_face_objects:
                return not context.scene.expresso_use_existing_armature

    def draw_assign_group_options(self, row, grp_name, grp_name_ui, can_pick=True, is_pivot_group=False, picker_running=False):
        # vgroup_names = get_list_expresso_groups()
        expresso_grp_name = 'expresso_' + grp_name
        is_assigned = expresso_grp_name in self.assigned_vertex_groups
        is_masked = f"Mask {expresso_grp_name}" in self.mask_modifiers
        mask_inverted = self.mask_modifiers.get(f"Mask {expresso_grp_name}", False)
        is_drawn = False
        single_surface = False
        additive_group = False
        if 'main' in grp_name:
            row.operator('expresso.assign_main', text=grp_name_ui, icon='GROUP_VERTEX')
            single_surface = True
            additive_group = True
        else:
            op = row.operator('expresso.assign_group', text=grp_name_ui,
                              icon='GROUP_VERTEX')
            op.vertex_group = grp_name
            op.is_pivot_group = is_pivot_group
        if can_pick:
            op = row.operator('expresso.vertex_group_picker', text='', icon='EYEDROPPER', depress=picker_running)
            op.vertex_group_name = grp_name
            op.single_surface = single_surface
            op.additive_group = additive_group
        sub = row.row(align=True)
        sub.enabled = is_assigned
        op = sub.operator('expresso.draw_expresso_vertex_group', text='',
                          icon='HIDE_OFF', depress=is_drawn)
        op.expresso_vertex_group_name = 'expresso_' + grp_name
        op = sub.operator('expresso.mask_group', text='', icon='MOD_MASK',
                          depress=is_masked)
        op.vgroup_name = 'expresso_' + grp_name
        op.operation = 'REMOVE' if is_masked else 'ADD'
        if is_masked:
            op = sub.operator('expresso.mask_group', text='', icon='ARROW_LEFTRIGHT',
                              depress=mask_inverted)
            op.vgroup_name = 'expresso_' + grp_name
            op.operation = 'INVERT'
        sub.operator('expresso.remove_expresso_groups', text='',
                     icon='X').vgroup_name = 'expresso_' + grp_name

    def get_all_mask_modifiers(self, objects):
        mask_modifiers = {}
        for obj in objects:
            for mod in obj.modifiers:
                if mod.type == 'MASK':
                    if 'expresso' in mod.name:
                        mask_modifiers[mod.name] = mod.invert_vertex_group
                        continue
        return mask_modifiers

    def draw(self, context):
        layout = self.layout
        objects = futils.get_expresso_objects_list()
        self.assigned_vertex_groups = vg_utils.get_assigned_expresso_vertex_groups(objects=objects)
        self.mask_modifiers = self.get_all_mask_modifiers(objects=objects)
        box = layout.box()
        coll_pick = box.column(align=True)
        picker_options = context.scene.expresso_picker_options
        picking_group = picker_options.picking_group
        row = coll_pick.row(align=True)
        row.label(text='Picker Options', icon='EYEDROPPER')
        row = coll_pick.row(align=True)
        row.prop(picker_options, 'pick_geometry', expand=True)
        row = coll_pick.row(align=True)
        row.prop(picker_options, 'hide_assigned', icon='HIDE_OFF', toggle=True)
        box = layout.box()
        col_main = box.column(align=True)
        row = col_main.row(align=True)
        row.label(text='Face Main (Mandatory)')
        row = col_main.row(align=True)
        row = col_main.row(align=True)

        self.draw_assign_group_options(
            row,
            'main',
            'Main',
            can_pick=True,
            picker_running=picking_group == 'main',
        )
        box = layout.box()
        col = box.column(align=True)
        separate_factor = .3
        col.separator(factor=separate_factor)
        col.label(text='Eyes (Eyeballs, Cornea, Iris, Spots, Highlights)')

        grid = col.grid_flow(columns=2, align=False)
        row = grid.row(align=True)
        self.draw_assign_group_options(row, 'right_eyes_other', 'Right Eye',
                                       is_pivot_group=True, picker_running=picking_group == 'right_eyes_other')

        row = grid.row(align=True)
        self.draw_assign_group_options(row, 'left_eyes_other', 'Left Eye', is_pivot_group=True,
                                       picker_running=picking_group == 'left_eyes_other')

        col.separator(factor=separate_factor)
        col.label(text='Teeth, Gum')

        row = col.row(align=True)
        self.draw_assign_group_options(
            row,
            'upper_teeth',
            'Upper Teeth',
            picker_running=picking_group == 'upper_teeth'
        )

        row = col.row(align=True)
        self.draw_assign_group_options(
            row,
            'lower_teeth',
            'Lower Teeth',
            picker_running=picking_group == 'lower_teeth'
        )

        # Tongue
        col.separator(factor=separate_factor)
        col.label(text='Tongue')

        row = col.row(align=True)
        self.draw_assign_group_options(
            row,
            'tongue',
            'Tongue',
            picker_running=picking_group == 'tongue'
        )

        # Eyelashes
        col.separator(factor=separate_factor)
        col.label(text='Eyelashes, Eyeshells, Tearlines')

        row = col.row(align=True)
        self.draw_assign_group_options(
            row,
            'eyelashes',
            'Eyelashes',
            picker_running=picking_group == 'eyelashes'
        )

        # Facial Hair
        col.separator(factor=separate_factor)
        col.label(text='Eyebrows, Beards, Facial Hair etc.')

        row = col.row(align=True)
        self.draw_assign_group_options(
            row,
            'facial_hair',
            'Facial Hair',
            picker_running=picking_group == 'facial_hair'
        )

        # Rigid
        col.separator(factor=separate_factor)
        col.label(text='Rigid, No Deform')

        row = col.row(align=True)
        self.draw_assign_group_options(
            row,
            'rigid',
            'Rigid',
            picker_running=picking_group == 'rigid'
        )

        if context.object:
            if context.object.mode != 'OBJECT':
                if context.object.type != 'MESH':
                    layout.enabled = False

        box = layout.box()
        col_utils = box.column(align=True)
        row = col_utils.row(align=True)
        row.label(text='Utilities')
        row = col_utils.row(align=True)
        row.operator('expresso.draw_expresso_vertex_group', text='Show Unassigned',
                     icon='HIDE_OFF', depress=False).expresso_vertex_group_name = 'UNASSIGNED'
        col_utils.separator()
        row = col_utils.row(align=True)
        row.operator('expresso.remove_all_expresso_groups', text='Reset All', icon='TRASH')


class FACE_OBJECTS_UL_list(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        scene = context.scene
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            obj = futils.get_object(item.name)
            row = layout.row(align=True)
            sub = row.row(align=True)
            sub.label(text=item.name, icon='OUTLINER_OB_MESH')
            if obj:
                if vg_utils.get_expresso_vertex_grps(obj):
                    row.operator('expresso.draw_assigned_groups_list', text='', icon='GROUP_VERTEX').obj_name = item.name
                if futils.get_hide_obj(obj):
                    sub.enabled = False
            if item.warnings and scene.expresso_show_warnings:
                op = row.operator('expresso.face_object_warning', text='', icon='ERROR')
                op.item_name = item.name
            op = row.operator('expresso.remove_facial_part', text='', icon='X')
            op.prompt = False
            op.remove_item = item.name
        else:
            layout.alignment = 'CENTER'
            layout.label(text='',)


class EXPRESSO_MT_ExpressoObjects(bpy.types.Menu):
    bl_label = "Expresso Register Options"

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        op = row.operator('expresso.clear_expresso_objects', text='Clear all Registered Objects', icon='TRASH')
        row = layout.row(align=True)
        row.operator('expresso.remove_all_expresso_groups', text='Reset All Vertex Groups', icon='TRASH')
        # op = row.operator('expresso.remove_expresso_groups', text='Reset All Vertex Groups', icon='TRASH')
        op.all_groups = True


class EXPRESSO_OT_DrawAssignedGroupsList(bpy.types.Operator):
    bl_label = "Assigned Groups"
    bl_idname = 'expresso.draw_assigned_groups_list'

    obj_name: StringProperty()

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self)

    def draw(self, context):

        layout = self.layout
        obj = futils.get_object(self.obj_name)
        if obj:
            expresso_groups = vg_utils.get_expresso_vertex_grps(obj)
            if expresso_groups:
                layout.label(text='Expresso Vertex Groups')

                box = layout.box()
                col = box.column()

                index = context.scene.expresso_face_objects.find(self.obj_name)
                for fgroup in expresso_groups:

                    row = col.row(align=True)
                    op = row.operator('expresso.remove_expresso_group_list', text='', icon='X')
                    op.vgroup_name = fgroup
                    op.object_list_index = index
                    op = row.operator('expresso.select_expresso_groups', text='', icon='EDITMODE_HLT')
                    op.expresso_vertex_group_name = fgroup
                    op.object_list_index = index
                    row.label(text=fgroup)

    def execute(self, context):
        return {'FINISHED'}
