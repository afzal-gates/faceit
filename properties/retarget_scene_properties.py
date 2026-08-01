import bpy
from bpy.props import (BoolProperty, CollectionProperty, EnumProperty,
                       IntProperty, PointerProperty, StringProperty)
from bpy.types import PropertyGroup, Scene

from ..core.retarget_list_base import FaceRegionsBase, RetargetShapesBase


class RetargetShapes(RetargetShapesBase, PropertyGroup):

    name: StringProperty(
        name='ARKit Expression',
        description='The ARKit Expression Name (Source Shape)',
        options=set(),
    )

    display_name: StringProperty(
        name='ARKit Expression',
        description='The ARKit Expression Display Name (Source Shape)',
        options=set(),
    )


def update_retargeting_scheme(self, context):
    if context is None:
        return
    if self.expresso_arkit_retarget_shapes:
        bpy.ops.expresso.change_retargeting_name_scheme()


def update_retarget_index(self, context):
    if context is None:
        return
    active_shape_item = None
    if self.expresso_display_retarget_list == 'ARKIT':
        if self.expresso_arkit_retarget_shapes:
            active_shape_item = self.expresso_arkit_retarget_shapes[self.expresso_arkit_retarget_shapes_index]
    else:
        if self.expresso_a2f_retarget_shapes:
            active_shape_item = self.expresso_a2f_retarget_shapes[self.expresso_a2f_retarget_shapes_index]

    if active_shape_item:
        shape_name = active_shape_item.name
        bpy.ops.expresso.set_active_shape_key_index(
            'EXEC_DEFAULT',
            shape_name=shape_name,
            get_active_target_shapes=True,
            amplify=active_shape_item.amplify,
        )


def register():
    ############## Retargeting Shapes ##################

    Scene.expresso_arkit_retarget_shapes = CollectionProperty(
        name='ARKIT Target Expressions',
        type=RetargetShapes,
    )

    Scene.expresso_arkit_retarget_shapes_index = IntProperty(
        name='Expression Index',
        default=0,
        update=update_retarget_index,
        options=set(),
    )
    Scene.expresso_a2f_retarget_shapes = CollectionProperty(
        name='Audio2Face Target Expressions',
        type=RetargetShapes,
    )
    Scene.expresso_a2f_retarget_shapes_index = IntProperty(
        name='Expression Index',
        default=0,
        update=update_retarget_index,
        options=set(),
    )

    Scene.expresso_face_regions = PointerProperty(
        name='Face Regions',
        type=FaceRegionsBase,
    )
    Scene.expresso_display_retarget_list = EnumProperty(
        items=(
            ('ARKIT', 'ARKit', 'ARKit Native'),
            ('A2F', 'Audio2Face', 'Nvidia Audio2Face'),
        ),
        default='ARKIT',
    )
    Scene.expresso_retargeting_naming_scheme = EnumProperty(
        items=(
            ('ARKIT', 'ARKit Native', 'ARKit Native'),
            ('FACECAP', 'FaceCap', 'bannaflak FaceCap'),
        ),
        default='ARKIT',
        update=update_retargeting_scheme,
    )


def unregister():
    del Scene.expresso_face_regions
    del Scene.expresso_arkit_retarget_shapes
    del Scene.expresso_arkit_retarget_shapes_index
    del Scene.expresso_a2f_retarget_shapes
    del Scene.expresso_a2f_retarget_shapes_index
    del Scene.expresso_retargeting_naming_scheme
