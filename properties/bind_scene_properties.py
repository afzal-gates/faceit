from bpy.props import (BoolProperty)
from bpy.types import Scene


def register():

    Scene.expresso_weights_restorable = BoolProperty(
        default=False,
    )
    Scene.expresso_expressions_restorable = BoolProperty(
        default=False,
    )
    Scene.expresso_corrective_sk_restorable = BoolProperty(
        default=False,
    )


def unregister():
    del Scene.expresso_weights_restorable
    del Scene.expresso_expressions_restorable
    del Scene.expresso_corrective_sk_restorable
