import bpy
from . import prop_rigger
from . import mesh_scanner
from . import create_pivot

bl_info = {
    "name": "Prop Rigger",
    "blender": (2, 80, 0),
    "category": "Object",
}


def register():
    bpy.utils.register_class(prop_rigger.PropRiggerPanel)
    bpy.utils.register_class(prop_rigger.MakePropRig)
    bpy.utils.register_class(create_pivot.RegionItem)
    bpy.utils.register_class(create_pivot.CreatePivot)
    bpy.utils.register_class(mesh_scanner.ScanMeshes)


def unregister():
    bpy.utils.unregister_class(prop_rigger.PropRiggerPanel)
    bpy.utils.unregister_class(prop_rigger.MakePropRig)
    bpy.utils.unregister_class(create_pivot.RegionItem)
    bpy.utils.unregister_class(create_pivot.CreatePivot)
    bpy.utils.unregister_class(mesh_scanner.ScanMeshes)


if __name__ == "__main__":
    register()
