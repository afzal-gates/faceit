

from bpy.props import BoolProperty
from bpy.types import Scene


def register():

    Scene.expresso_shapes_generated = BoolProperty(
        name='Generated Shape Keys',
        default=False,
    )


def unregister():
    del Scene.expresso_shapes_generated
