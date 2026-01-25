import bpy


class RegionItem(bpy.types.PropertyGroup):
    obj: bpy.props.PointerProperty(
        name="Object",
        type=bpy.types.Object
    )


class CreatePivot(bpy.types.Operator):
    bl_idname = "wm.create_pivot"
    bl_label = "Creates an empty with unique collection properties"

    bone_type: bpy.props.EnumProperty(
        name="Bone Type",
        description="Choose the type of bone to add",
        items=[
            ('ROOT', "Root", "Root bone in mesh"),
            ('CHAIN', "Chain", "Bone in a chain, has no control gizmo"),
            ('HINGE', "Hinge", "Bone that moves on a hinge")
        ]
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        cursor_loc = bpy.context.scene.cursor.location
        bpy.ops.object.empty_add(type='SINGLE_ARROW', location=cursor_loc)

        bpy.types.Object.region_group = bpy.props.CollectionProperty(
            type=RegionItem)
        pivot = bpy.context.object
        pivot.name = self.bone_type+"_Pivot"
        pivot["bone_type"] = self.bone_type

        return {'FINISHED'}
