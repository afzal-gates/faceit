from bpy.props import (BoolProperty, EnumProperty, PointerProperty,
                       StringProperty)
from bpy.types import PropertyGroup, Scene

workspace_tab_dict = {
    'ALL': (
        ('SETUP', 'Setup', 'Setup Tab'),
        ('CREATE', 'Rig', 'Create Tab'),
        ('EXPRESSIONS', 'Expressions', 'Expressions Tab'),
        ('BAKE', 'Bake', 'Bake Tab'),
        ('SHAPES', 'Shapes', 'Target Shape Keys Settings'),
        ('CONTROL', 'Control', 'Control Rig'),
        ('MOCAP', 'Mocap', 'Motion Capture'),
    ),
    'RIG': (
        ('SETUP', 'Setup', 'Setup Tab'),
        ('CREATE', 'Rig', 'Create Tab'),
        ('EXPRESSIONS', 'Expressions', 'Expressions Tab'),
        ('BAKE', 'Bake', 'Bake Tab'),
    ),
    'MOCAP': (
        ('SETUP', 'Setup', 'Setup Tab'),
        ('SHAPES', 'Shapes', 'Target Shape Keys Settings'),
        ('CONTROL', 'Control', 'Control Rig'),
        ('MOCAP', 'Mocap', 'Motion Capture'),
    )
}


def _get_tab_items_from_workspace(self, context):
    workspaces = workspace_tab_dict[self.workspace]
    if context.scene.expresso_use_existing_armature:
        # remove the create tab
        workspaces = [w for w in workspaces if w[0] != 'CREATE']
    return workspaces


def update_tab(self, context):
    if context is None:
        return
    if self.workspace == 'ALL':
        self.all_tab = self.active_tab
    elif self.workspace == 'RIG':
        self.rig_tab = self.active_tab
    elif self.workspace == 'MOCAP':
        self.mocap_tab = self.active_tab


def update_workspace(self, context):
    if self.workspace == 'ALL':
        self.active_tab = self.all_tab
    elif self.workspace == 'RIG':
        self.active_tab = self.rig_tab
    elif self.workspace == 'MOCAP':
        self.active_tab = self.mocap_tab


class PinPanels(PropertyGroup):
    # Setup
    EXPRESSO_PT_SetupRegister: BoolProperty()
    EXPRESSO_PT_SetupVertexGroups: BoolProperty()
    EXPRESSO_PT_BodyRigSetup: BoolProperty()
    # Rigging
    EXPRESSO_PT_Rigging: BoolProperty()
    EXPRESSO_PT_Landmarks: BoolProperty()
    # Expressoins
    EXPRESSO_PT_Expressions: BoolProperty()
    EXPRESSO_PT_ExpressionOptions: BoolProperty()
    # Bake Panel (Utils)
    EXPRESSO_PT_BakeExpressions: BoolProperty()
    EXPRESSO_PT_ShapeKeyUtils: BoolProperty()
    EXPRESSO_PT_RigUtils: BoolProperty()
    EXPRESSO_PT_Other: BoolProperty()
    # ARKit Shapes
    EXPRESSO_PT_TargetShapeLists: BoolProperty()
    EXPRESSO_PT_RetargetShapesSetup: BoolProperty()
    # Control Rig
    EXPRESSO_PT_ControlRig: BoolProperty()
    EXPRESSO_PT_ControlRigSettings: BoolProperty()
    EXPRESSO_PT_ControlRigAnimation: BoolProperty()
    EXPRESSO_PT_ControlRigUtils: BoolProperty()
    EXPRESSO_PT_ControlRigTargetShapes: BoolProperty()
    EXPRESSO_PT_ControlRigTargetObjects: BoolProperty()
    # Mocap
    EXPRESSO_PT_MocapUtils: BoolProperty()
    EXPRESSO_PT_MocapImporters: BoolProperty()
    EXPRESSO_PT_MocapLive: BoolProperty()
    EXPRESSO_PT_MocapSetup: BoolProperty()
    EXPRESSO_PT_RetargetFBX: BoolProperty()

    def get_pin(self, panel_idname):
        return getattr(self, panel_idname, 0)


class ExpressoWorkspace(PropertyGroup):
    name: StringProperty()
    workspace: EnumProperty(
        name='The Active Expresso Workspace',
        items=(
            ('ALL', 'All', 'Choose this option if you want to have all functionality available.'),
            ('RIG', 'Rig', 'Chosse this option if you only want to create blendshapes. Motion Capture Utils are hidden.'),
            ('MOCAP', 'Mocap', 'Choose this option when your geometry has blendshapes and you only want to do Motion Capture'),
        ),
        default='ALL',
        update=update_workspace,
    )
    active_tab: EnumProperty(
        items=_get_tab_items_from_workspace,
        update=update_tab,
    )
    all_tab: StringProperty(
        default='SETUP',
        description='The active tab when the ALL workspace.'
    )
    rig_tab: StringProperty(
        default='SETUP',
        description='The active tab when the RIG workspace.'
    )
    mocap_tab: StringProperty(
        default='SETUP',
        description='The active tab in the MOCAP Workspace',
    )
    expand_ui: BoolProperty()


# --------------- REGISTER/UNREGISTER --------------------
# |
# --------------------------------------------------------


def register():

    Scene.expresso_workspace = PointerProperty(
        type=ExpressoWorkspace,
    )
    Scene.expresso_expression_init_expand_ui = BoolProperty(
        name='Initialize',
        default=True
    )
    Scene.expresso_pin_panels = PointerProperty(
        name='Pin Props',
        type=PinPanels,
    )


def unregister():
    del Scene.expresso_workspace
    del Scene.expresso_expression_init_expand_ui
    del Scene.expresso_pin_panels
