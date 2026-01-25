import bpy
from . import blender_util as util


# redundant name but mandatory
class PivotName(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()


class MeshScanData(bpy.types.PropertyGroup):
    scan_volume: bpy.props.PointerProperty(type=util.RegionBox)
    pivots: bpy.props.CollectionProperty(type=PivotName)


class ScanMeshes(bpy.types.Operator):
    bl_idname = "wm.mesh_scanner"
    bl_label = "Scan selected meshes and pair them with the appropriate pivot"

    def execute(self, context):
        mesh_objs = []
        for obj in bpy.context.selected_objects:
            if type(obj.data) is bpy.types.Mesh:
                mesh_objs.append(obj)

        main_box = util.get_box(mesh_objs)
        pivots = util.get_pivots(main_box)

        if len(pivots) >= 1:
            self._cache_meshes_by_region(mesh_objs, pivots)

        scan = bpy.context.scene.mesh_scan

        scan.scan_volume.origin = main_box.origin
        scan.scan_volume.half_size = main_box.half_size
        return {'FINISHED'}

    def _cache_meshes_by_region(self, objs, pivots):
        scan = bpy.context.scene.mesh_scan
        for obj in objs:
            box = util.get_box([obj])

            # sort regions by how close they are
            regions = pivots.copy()
            regions.sort(
                key=(lambda r: (obj.location - r.location).magnitude)
            )
            print(regions)

            if regions is not None:
                if len(regions) >= 1:
                    print("added ", obj, "\nto ", regions[0])
                    pivot = scan.pivots.add()
                    pivot.name = regions[0].name
                    new_item = regions[0].region_group.add()
                    new_item.obj = obj

                for r in range(1, len(regions)):
                    if util.is_in_box(regions[r].location, box):
                        print("added ", obj, "\nto ", regions[r])
                        pivot = scan.pivots.add()
                        pivot.name = regions[r].name
                        new_item = regions[r].region_group.add()
                        new_item.obj = obj

        print("----------")
        print("")
