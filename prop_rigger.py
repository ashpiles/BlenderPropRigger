import bpy
from . import bone_setup as bs


class MakePropRig(bpy.types.Operator):
    """Creates new armature from selected objects from bone_type"""
    bl_idname = "wm.prop_auto_rig"
    bl_label = "Make prop Auto Rig"

    def execute(self, context):
        bpy.ops.wm.mesh_scanner()
        setup_routine = {
            'ROOT':     [],
            'STANDARD': [],
            'CHAIN':    [],
            'SLIDE':    [],
            'SQUISH':   [],
            'SPIN':     [],
            'HINGE':    []
        }

        scan_result = bpy.context.scene.mesh_scan
        armature = bpy.data.armatures.new("Prop_Armature")
        rig = bpy.data.objects.new("Prop_Armature", armature)
        bpy.context.collection.objects.link(rig)

        bpy.context.view_layer.objects.active = rig
        bpy.ops.object.mode_set(mode='EDIT')

        print(scan_result.pivots)
        # consume pivots to create respective set-up objects
        # in given order for correct rig creation
        for region in scan_result.pivots:
            try:
                pivot = bpy.context.collection.objects[region.name]
            except KeyError:
                pivot = None

            if pivot is not None:
                bone_type = pivot['bone_type']
                setup = bs.RootBoneSetup(pivot)
                setup_routine[bone_type].append(setup)

        print(setup_routine)
        print(setup_routine.items())
        # consume setup objects to create rig
        for setup_type, setups in setup_routine.items():
            print(setup_type, setups)
            for setup in setups:
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
