import bpy
import re
from mathutils import Vector
from . import blender_util as util


class ScanMeshes(bpy.types.Operator):
    bl_idname = "wm.scan_meshes"
    bl_label = "Scan selected meshes"

    def execute(self, context):
        pivots = []
        for obj in bpy.context.scene.objects:
            pivot_search = re.compile(r'Pivot($|\.\d+)')
            if obj.data is None and pivot_search.search(obj.name) is not None:
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
        filtered_pivots = filter(
            lambda p: util.is_in_box(p.location, main_box), pivots)
        regions = list(filtered_pivots)

        print(main_box)
        for obj in objs:
            box = util.get_box([obj])
            box_c, box_s = box

            regions = self.sort_regions(obj.location, regions)

            print(box_c, box_s)

            if regions is not None:
                if len(regions) >= 1:
                    print("added ", obj, "\nto ", regions[0])
                    new_item = regions[0].region_group.add()
                    new_item.obj = obj

                for r in range(1, len(regions)):
                    if util.is_in_box(regions[r].location, box):
                        print("added ", obj, "\nto ", regions[r])
                        new_item = regions[r].region_group.add()
                        new_item.obj = obj

        print("----------")
        print("")

    def sort_regions(self, vert: Vector, regions: list):
        regions.sort(key=lambda p: (vert - p.location).magnitude)

        return regions
