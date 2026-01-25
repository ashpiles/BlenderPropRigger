import bpy
from . import blender_util as util
from . import prop_rigger
from . import mesh_scanner
from . import create_pivot

bl_info = {
    "name": "Prop Rigger",
    "blender": (2, 80, 0),
    "category": "Object",
}


def register():
    bpy.utils.register_class(util.RegionBox)
    bpy.utils.register_class(prop_rigger.PropRiggerPanel)
    bpy.utils.register_class(prop_rigger.MakePropRig)
    bpy.utils.register_class(create_pivot.RegionItem)
    bpy.utils.register_class(create_pivot.CreatePivot)
    bpy.utils.register_class(mesh_scanner.ScanMeshes)
    bpy.utils.register_class(mesh_scanner.PivotName)
    bpy.utils.register_class(mesh_scanner.MeshScanData)

    bpy.types.Scene.region_boxes = bpy.props.CollectionProperty(
        type=util.RegionBox
    )
    bpy.types.Scene.mesh_scan = bpy.props.PointerProperty(
        type=mesh_scanner.MeshScanData
    )


def unregister():
    del bpy.types.Scene.mesh_scan
    del bpy.types.Scene.region_boxes

    bpy.utils.unregister_class(util.RegionBox)
    bpy.utils.unregister_class(prop_rigger.PropRiggerPanel)
    bpy.utils.unregister_class(prop_rigger.MakePropRig)
    bpy.utils.unregister_class(create_pivot.RegionItem)
    bpy.utils.unregister_class(create_pivot.CreatePivot)
    bpy.utils.unregister_class(mesh_scanner.ScanMeshes)
    bpy.utils.unregister_class(mesh_scanner.PivotName)
    bpy.utils.unregister_class(mesh_scanner.MeshScanData)


if __name__ == "__main__":
    register()
