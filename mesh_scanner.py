import bpy
from . import blender_util as util


class ScanMeshes():
    def __init__(self):
        mesh_objs = []

        for obj in bpy.context.selected_objects:
            if type(obj.data) is bpy.types.Mesh:
                mesh_objs.append(obj)

        self.main_box = util.get_box(mesh_objs)
        self.pivots = util.get_pivots(self.main_box)
        # seems to work on the first attempt or randomly doesn't work
        # the working context might not be properly cleared

        if len(self.pivots) >= 1:
            self._cache_meshes_by_region(mesh_objs, self.pivots)

    def _add_to_region(self, obj, region):
        if region.name != "ROOT_Pivot" and obj is not None:
            print("added ", obj, "\nto ", region)
            new_item = region.region_group.add()
            new_item.obj = obj

    def _cache_meshes_by_region(self, objs, pivots):
        # Hacky fix for including root
        root = None
        for pivot in pivots:
            if pivot.name == "ROOT_Pivot":
                root = pivot
                pivots.remove(pivot)
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
                    self._add_to_region(obj, regions[0])

                for r in range(1, len(regions)):
                    if util.is_in_box(regions[r].location, box):
                        self._add_to_region(obj, regions[r])

        pivots.append(root)
        print("----------")
        print("")
