import bpy
from mathutils import Vector
from . import blender_util as util


class ScanMeshes(bpy.types.Operator):
    bl_idname = "wm.scan_meshes"
    bl_label = "Scan selected meshes"

    def execute(self, context):
        pivots = []
        for obj in bpy.context.scene.objects:
            if obj.data is None and obj.name.endswith("Pivot"):
                pivots.append(obj)

        mesh_objs = []
        for obj in bpy.context.selected_objects:
            if type(obj.data) is bpy.types.Mesh:
                mesh_objs.append(obj)

        if len(pivots) >= 1:
            self._cache_meshes_by_region(mesh_objs, pivots)

        return {'FINISHED'}

    def _cache_meshes_by_region(self, objs, pivots):
        main_box = util.get_box(objs)
        for p_index in range(0, len(pivots)):
            if not util.is_in_box(pivots[p_index].location, main_box):
                pivots.pop(p_index)

        for obj in objs:
            box_c, box_s = util.get_box([obj])

            regions = self.sort_regions(obj.location, main_box, pivots)

            print(box_c, box_s)
            print(obj, regions)
            print("----------")

            if regions is not None:
                if len(regions) >= 1:
                    new_item = regions[0].region_group.add()
                    new_item.obj = obj

                for r in range(1, len(regions)):
                    if util.is_in_box(regions[r].location, box_c, box_s):
                        new_item = regions[r].region_group.add()
                        new_item.obj = obj

    def sort_regions(self, vert: Vector, box, regions: list):
        if (not util.is_in_box(vert, box)):
            return

        regions.sort(key=lambda p: (vert - p.location).magnitude)

        return regions
