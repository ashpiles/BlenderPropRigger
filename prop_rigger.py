from . import blender_util as util
import bpy


class MakePropRig(bpy.types.Operator):
    """Creates new armature from selected objects from bone_type"""
    bl_idname = "wm.prop_auto_rig"
    bl_label = "Make prop Auto Rig"

    # this is making extras
    def execute(self, context):

        pivots = []
        pos, scale = util.get_mesh_info(bpy.context.selected_objects)

        armature = bpy.data.armatures.new("Gun_Armature")
        rig = bpy.data.objects.new("Gun_Armature", armature)

        bpy.context.collection.objects.link(rig)

        bpy.context.view_layer.objects.active = rig
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}


class PropRiggerPanel(bpy.types.Panel):
    """Creates a Panel in World View UI to gun Auto Rigging"""
    bl_label = "Prop Auto Rigger"
    bl_idname = "OBJECT_PT_prop_auto_rigger"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Create Prop Auto Rig", icon='ARMATURE_DATA')

        active_name = obj.name if obj else ""
        row = layout.row()
        row.label(text="Active object is: " + active_name)

        row = layout.row()
        row.operator("wm.create_pivot")

        row = layout.row()
        row.operator("wm.scan_meshes")
