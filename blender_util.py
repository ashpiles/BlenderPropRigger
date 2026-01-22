import bpy
import math
from mathutils import (
    Vector,
)


def select_bone(rig, name):
    bpy.ops.object.mode_set(mode='POSE')
    rig.data.bones.active = rig.data.bones[name]
    rig.pose.bones[name].bone.select = True


def lock_bone(rig, name):
    select_bone(rig, name)

    for l_index in range(len(bpy.context.active_pose_bone.lock_location)):
        bpy.context.active_pose_bone.lock_location[l_index] = True
    bpy.context.active_pose_bone.lock_rotation_w = True
    for r_index in range(len(bpy.context.active_pose_bone.lock_rotation)):
        bpy.context.active_pose_bone.lock_rotation[r_index] = True
    for s_index in range(len(bpy.context.active_pose_bone.lock_scale)):
        bpy.context.active_pose_bone.lock_scale[s_index] = True


def hide_bones(rig, hide_names):
    bpy.ops.object.mode_set(mode='POSE')

    for name in hide_names:
        rig.pose.bones[name].bone.hide = True


def set_bone_rot(bone_name, rot):
    bpy.ops.object.mode_set(mode='POSE')
    arm_obj = bpy.context.object

    pb = arm_obj.pose.bones[bone_name]
    arm_obj.data.bones.active = pb.bone

    pb.rotation_quaternion = rot


def iter_mesh_objects(obj):
    if obj.type == 'MESH':
        yield obj
    for child in obj.children_recursive:
        if child.type == 'MESH':
            yield child


# you can parent with AUTOMATIC_WEIGHTS
# so what i need is a way to figure out the range we are
# parenting bones
def parent_bones(rig, parent, child, is_offset=True):
    bpy.ops.object.mode_set(mode='EDIT')

    ebones = rig.data.edit_bones

    # Clear selection explicitly
    for b in ebones:
        b.select = False
        b.select_head = False
        b.select_tail = False

    # Select child first
    ebones[child].select = True

    # Select + activate parent LAST
    ebones[parent].select = True
    ebones.active = ebones[parent]

    if is_offset:
        bpy.ops.armature.parent_set(type='OFFSET')
    else:
        bpy.ops.armature.parent_set(type='CONNECTED')


def get_box(objs: list):
    min_v = Vector((math.inf, math.inf, math.inf))
    max_v = Vector((-math.inf, -math.inf, -math.inf))

    for obj in objs:
        for mesh_obj in iter_mesh_objects(obj):
            for corner in mesh_obj.bound_box:
                world_corner = mesh_obj.matrix_world @ Vector(corner)
                min_v.x = min(min_v.x, world_corner.x)
                min_v.y = min(min_v.y, world_corner.y)
                min_v.z = min(min_v.z, world_corner.z)

                max_v.x = max(max_v.x, world_corner.x)
                max_v.y = max(max_v.y, world_corner.y)
                max_v.z = max(max_v.z, world_corner.z)

    center = (min_v + max_v) * 0.5
    half_size = (max_v - min_v) * 0.5
    return center, half_size


def is_in_box(point: Vector, box: tuple):
    origin, half_size = box
    return (
        origin.x - half_size.x <= point.x <= origin.x + half_size.x and
        origin.y - half_size.y <= point.y <= origin.y + half_size.y and
        origin.z - half_size.z <= point.z <= origin.z + half_size.z
    )
