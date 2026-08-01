import bpy

from .. import __package__ as base_package
from ..core import expresso_utils as futils
from . import draw_utils


class EXPRESSO_PT_Base():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EXPRESSO'
    bl_label = 'Base'
    bl_options = {'DEFAULT_CLOSED'}

    expresso_predecessor = 'EXPRESSO_PT_MainPanel'
    UI_TABS = ('SETUP',)
    UI_WORKSPACES = ('ALL', 'RIG', 'MOCAP')
    weblink = "https://expresso-doc.readthedocs.io/en/latest/"

    @classmethod
    def poll(cls, context):
        workspace = context.scene.expresso_workspace
        if workspace.workspace in cls.UI_WORKSPACES:
            pin_panel = bpy.context.scene.expresso_pin_panels
            return workspace.active_tab in cls.UI_TABS or pin_panel.get_pin(
                cls.bl_idname)

    def draw_header_preset(self, context):
        row = self.layout.row()
        pin_panel = bpy.context.scene.expresso_pin_panels

        if pin_panel.get_pin(self.bl_idname):
            if context.scene.expresso_workspace.active_tab not in self.UI_TABS:
                row.label(text=self.UI_TABS[0])
            icon = 'PINNED'
        else:
            icon = 'UNPINNED'
        row.prop(pin_panel, self.bl_idname, text='', emboss=False, icon=icon)
        if self.weblink and context.preferences.addons[base_package].preferences.web_links:
            draw_utils.draw_web_link(
                layout=row,
                link=self.weblink,
            )
        if self.use_pin:
            row.label(text="", icon='BLANK1')

    def draw(self, context):
        pass


class EXPRESSO_PT_BaseSub():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EXPRESSO'
    bl_label = 'Base Sub'
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = ''
    expresso_predecessor = ''
    weblink = ""

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout

    def draw_header_preset(self, context):
        row = self.layout.row()
        if self.weblink and context.preferences.addons[base_package].preferences.web_links:
            draw_utils.draw_web_link(
                layout=row,
                link=self.weblink,
            )


class EXPRESSO_PT_MainPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'EXPRESSO'
    bl_label = 'Expresso'
    bl_idname = 'EXPRESSO_PT_MainPanel'
    # bl_options = {'HIDE_HEADER'}
    bl_order = 0

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        box = layout.box()
        row = box.row()
        expresso_workspace = scene.expresso_workspace
        if expresso_workspace.expand_ui:
            icon = 'TRIA_DOWN'
        else:
            icon = 'TRIA_RIGHT'
        row.prop(expresso_workspace, 'expand_ui', text='Choose Workspace',
                 icon=icon, icon_only=True, emboss=False)
        if expresso_workspace.expand_ui:
            box.row().prop(expresso_workspace, 'workspace', expand=True, icon='CUBE')
        active_tab = expresso_workspace.active_tab
        layout.row().prop(expresso_workspace, 'active_tab', expand=True)
        layout.separator()
        rig = context.scene.expresso_armature
        if active_tab != 'SETUP':
            if not scene.expresso_face_objects and not scene.expresso_control_armature:
                col = layout.column()
                row = col.row()
                row.alert = True
                op = row.operator('expresso.go_to_tab', text='Complete Setup First...')
                op.tab = 'SETUP'
                return
        if active_tab in ('CONTROL', 'MOCAP'):
            if not scene.expresso_arkit_retarget_shapes and not scene.expresso_arkit_retarget_shapes and not scene.expresso_control_armature:
                col = layout.column()
                row = col.row()
                row.alert = True
                op = row.operator('expresso.go_to_tab', text='No Targets Shapes found...')
                op.tab = 'SHAPES'
                return
            if active_tab == 'CONTROL':
                if scene.expresso_face_objects:
                    col = layout.column()
                    if scene.expresso_pin_panels.EXPRESSO_PT_Landmarks:
                        icon = 'PINNED'
                    else:
                        icon = 'UNPINNED'
                    row = col.row()
                    row.prop(scene, "expresso_show_landmarks_ctrl_rig", text="Show Landmark Panel", icon=icon)

        elif active_tab in ('EXPRESSIONS', 'BAKE', 'CREATE'):
            if rig is None:
                if scene.expresso_armature_missing:
                    col = layout.column()
                    row = col.row()
                    row.alert = True
                    row.label(text="Warning: The Expresso Rig has been deleted.")
                if active_tab != 'CREATE':
                    col = layout.column()
                    row = col.row()
                    row.alert = True
                    op = row.operator('expresso.go_to_tab', text='Generate Rig First...')
                    op.tab = 'CREATE'
            elif active_tab == 'BAKE':
                if 'overwrite_shape_action' not in bpy.data.actions or not scene.expresso_expression_list:
                    col = layout.column()
                    row = col.row()
                    row.alert = True
                    op = row.operator('expresso.go_to_tab', text='Generate Expressions First...')
                    op.tab = 'EXPRESSIONS'

        if futils.get_any_view_locked():
            row = layout.row()
            row.operator("expresso.unlock_3d_view", icon='LOCKED', depress=True)
