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
        scan = bpy.context.scene.mesh_scan
        scan.pivots.clear()

        for obj in bpy.context.selected_objects:
            if type(obj.data) is bpy.types.Mesh:
                mesh_objs.append(obj)

        main_box = util.get_box(mesh_objs)
        pivots = util.get_pivots(main_box)

        if len(pivots) >= 1:
            self._cache_meshes_by_region(mesh_objs, pivots)

        scan.scan_volume.origin = main_box.origin
        scan.scan_volume.half_size = main_box.half_size
        return {'FINISHED'}

    def _add_to_region(self, obj, region):
        scan = bpy.context.scene.mesh_scan
        pivot = scan.pivots.add()
        pivot.name = region.name
        if region.name != "ROOT_Pivot" or obj is None:
            new_item = region.region_group.add()
            new_item.obj = obj

    def _cache_meshes_by_region(self, objs, pivots):
        for pivot in pivots:
            if pivot.name == "ROOT_Pivot":
                self._add_to_region(None, pivot)
                pivots.remove(pivot)

        for obj in objs:
            box = util.get_box([obj])

            # sort regions by how close they are
            regions = pivots.copy()
            regions.sort(
                key=(lambda r: (obj.location - r.location).magnitude)
            )

            if regions is not None:
                if len(regions) >= 1:
                    print("added ", obj, "\nto ", regions[0])
                    self._add_to_region(obj, regions[0])

                for r in range(1, len(regions)):
                    if util.is_in_box(regions[r].location, box):
                        print("added ", obj, "\nto ", regions[r])
                        self._add_to_region(obj, regions[r])

        print("----------")
        print("")
