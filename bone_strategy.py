import bpy
from . import blender_util as util
from mathutils import (
    Vector,
)


class BoneSetup():
    bone_type_desc = "default"

    def __init__(self, pivot):
        pivot.rotation_mode = 'QUATERNION'
        self.pivot_name = pivot.name
        self.loc = pivot.location
        self.rot = pivot.rotation_quaternion
        self.objs = pivot["bone_children"]
        self.length = pivot.empty_display_size

        pivot_obj = bpy.data.objects.get(self.pivot_name)
        bpy.data.objects.remove(pivot_obj, do_unlink=True)

    # virtual func
    def _bone_strategy(self, arm, rig):
        pass

    # apply rotation eventually
    def _make_bones(self, arm, bone_name):
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
            arm, self.bone_type+"_bone")

        # apply rotation

        util.set_bone_rot(def_name, self.rot)
        util.set_bone_rot(mch_name, self.rot)

        # Remove deforms of non-deform bones
        bpy.ops.object.mode_set(mode='POSE')
        rig.select_set(True)

        rig.data.bones.active = rig.data.bones[mch_name]
        rig.pose.bones[mch_name].bone.select = True
        bpy.context.active_bone.use_deform = False

        rig.pose.bones[ctrl_name].bone.select = True
        rig.data.bones.active = rig.data.bones[ctrl_name]
        bpy.context.active_bone.use_deform = False

        util.parent_bones(rig, 'root', mch_name)
        util.parent_bones(rig, mch_name, def_name)
        util.parent_bones(rig, 'root', ctrl_name)

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

        for obj in self.objs:
            if obj:
                obj.select_set(True)

        rig.select_set(True)
        bpy.context.view_layer.objects.active = rig

        rig.pose.bones[bone_name].bone.select = True

        rig.data.bones.active = rig.data.bones[bone_name]

        bpy.ops.object.parent_set(type='BONE', keep_transform=True)
