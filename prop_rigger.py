import bpy
from . import bone_setup


class MakePropRig(bpy.types.Operator):
    """Creates new armature from selected objects from bone_type"""
    bl_idname = "wm.prop_auto_rig"
    bl_label = "Make prop Auto Rig"

    def execute(self, context):
        bpy.ops.wm.mesh_scanner()

        scan_result = bpy.context.scene.mesh_scan
        armature = bpy.data.armatures.new("Prop_Armature")
        rig = bpy.data.objects.new("Prop_Armature", armature)
        bpy.context.collection.objects.link(rig)

        bpy.context.view_layer.objects.active = rig
        bpy.ops.object.mode_set(mode='EDIT')

        for region in scan_result.pivots:
            pivot = bpy.context.collection.objects[region.name]
            match pivot['bone_type']:
                case 'ROOT':
                    setup = bone_setup.RootBoneSetup(pivot)
                    setup.set_bone(armature, rig)
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
        row.operator("wm.prop_auto_rig")
