import bpy
from . import blender_util as util
from mathutils import (
    Vector,
)

# ensure we get all the info needed from pivot


class BoneSetup():
    bone_type_desc = "default"

    def __init__(self, pivot):
        # consume the pivot for other operations
        pivot.rotation_mode = 'QUATERNION'
        self.pivot_name = pivot.name
        self.bone_type = pivot['bone_type']
        self.loc = pivot.location
        self.rot = pivot.rotation_quaternion
        self.length = pivot.empty_display_size
        self.objs = [p.obj for p in list(pivot.region_group)]

        pivot_obj = bpy.data.objects.get(self.pivot_name)
        bpy.data.objects.remove(pivot_obj, do_unlink=True)

    # virtual func
    def _bone_strategy(self, arm, rig):
        pass

    # apply rotation eventually
    def _make_bones(self, bone_name, arm):
        bpy.ops.object.mode_set(mode='EDIT')
        def_bone = arm.edit_bones.new("DEF_"+bone_name)
        def_bone.head = self.loc
        def_bone.tail = self.loc + Vector((0, 0, self.length))

        mch_bone = arm.edit_bones.new("MCH_"+bone_name)
        mch_bone.head = self.loc
        mch_bone.tail = self.loc + Vector((0, 0, self.length))

        ctrl_bone = arm.edit_bones.new("CTRL_"+bone_name)
        ctrl_bone.head = self.loc
        ctrl_bone.tail = self.loc + Vector((0, 0, self.length))

        return (def_bone.name, mch_bone.name, ctrl_bone.name)

    def _basic_bone_setup(self, arm, rig):
        bpy.ops.object.mode_set(mode='EDIT')
        def_name, mch_name, ctrl_name = self._make_bones(
            self.bone_type+"_bone", arm,)
        # apply rotation
        util.set_bone_rot(def_name, self.rot)
        util.set_bone_rot(mch_name, self.rot)
        # Remove deforms of non-deform bones
        bpy.ops.object.mode_set(mode='POSE')
        rig.select_set(True)

        util.select_bone(rig, mch_name)
        bpy.context.active_bone.use_deform = False

        util.select_bone(rig, ctrl_name)
        bpy.context.active_bone.use_deform = False

        # need a better default root parenting startegy
        # util.parent_bones(rig, 'root', mch_name)
        # util.parent_bones(rig, mch_name, def_name)
        # util.parent_bones(rig, 'root', ctrl_name)

        # lock loc, scale, & rot of mch
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        util.lock_bone(rig, mch_name)
        util.lock_bone(rig, def_name)

        return (def_name, mch_name, ctrl_name)

    # Manages pivot input for bone creation/ parenting strategy
    def set_bone(self, arm, rig):
        bone = self._bone_strategy(arm, rig)
        if not bone:
            return

        bone_name = bone.name

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='POSE')

        # here i need a better setting strat
        # need to deal with sharing objs with another def bone
        for obj in self.objs:  # why do we have 2 of the same pivot?
            if obj is not None:
                print(obj)

        rig.select_set(True)
        bpy.context.view_layer.objects.active = rig
        util.select_bone(rig, bone_name)
        bpy.ops.object.parent_set(type='BONE', keep_transform=True)

# Check up on the armature creation

# root bone
# - denotes the root
# standard bone
# - does nothing special
# sliding bone
# - only slides
# hinge bone
# - rotates around a hinge
# spin bone
# - spins it self
# squish bone
# - controls scale


"""
the relationship between objs and regions are a bit complicated
As a region by default will have many objs to parent
however sometimes objs will share regions

to deal with this i will treat objects with multiple regions will
need to check if its the same type of region and then implement different
parenting strategies
for example if it is a different type then they should behave as normal
however if it is of the same type they must then skin with automatic weights
"""


class RootBoneSetup(BoneSetup):
    def __init__(self, pivot):
        super().__init__(pivot)

    def _bone_strategy(self, arm, rig):
        def_name, mch_name, ctrl_name = self._basic_bone_setup(arm, rig)

        bpy.ops.object.mode_set(mode='POSE')
        util.select_bone(rig, mch_name)

        bpy.ops.pose.constraint_add(type='COPY_LOCATION')
        constraint = bpy.context.object.pose.bones[mch_name].constraints["Copy Location"]
        constraint.target = rig
        constraint.subtarget = ctrl_name
        constraint.target_space = 'LOCAL'
        constraint.owner_space = 'LOCAL'

        util.select_bone(rig, mch_name)
        bpy.ops.pose.constraint_add(type='COPY_ROTATION')

        constraint = bpy.context.object.pose.bones[mch_name].constraints["Copy Rotation"]
        constraint.target = rig
        constraint.subtarget = ctrl_name
        constraint.mix_mode = 'BEFORE'
        constraint.target_space = 'LOCAL'
        constraint.owner_space = 'LOCAL'

        util.select_bone(rig, ctrl_name)
        # bpy.context.active_pose_bone.custom_shape = bpy.data.objects["Generic_Gizmo"]

        util.hide_bones(rig, [mch_name, def_name])

        bpy.ops.object.mode_set(mode='EDIT')
        return arm.edit_bones[def_name]
