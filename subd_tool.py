# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/1d_subd_tool
#
# Version history:
#   2022.03.20 - 1.0.0. - initial release

import bpy
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class


bl_info = {
    'name': 'SUBD_TOOL',
    'category': 'All',
    'author': 'Nikita Akimov',
    'version': (1, 0, 0),
    'blender': (2, 79, 0),
    'location': 'The 3D_View window - T-panel - the 1D tab',
    'wiki_url': 'https://github.com/Korchy/1d_subd_tool',
    'tracker_url': 'https://github.com/Korchy/1d_subd_tool',
    'description': 'Tool for work with objects with the Subdivision Surface modifier'
}


class SubdTool:

    @classmethod
    def store_subd(cls, context):
        # View to Render in Subdivision Modifier
        obj_subd = cls._sub_objects(context=context, selected=True)
        modifiers = (modifier for obj in obj_subd for modifier in obj.modifiers
                     if modifier.type == 'SUBSURF')
        for modifier in modifiers:
            modifier.render_levels = modifier.levels

    @classmethod
    def view_subd(cls, context):
        # Render to View in Subdivision Modifier
        obj_subd = cls._sub_objects(context=context, selected=True)
        modifiers = (modifier for obj in obj_subd for modifier in obj.modifiers
                     if modifier.type == 'SUBSURF')
        for modifier in modifiers:
            modifier.levels = modifier.render_levels

    @classmethod
    def select_subd(cls, context):
        # select objects with Render = Render in active object
        # render subdivision value from active object
        active_object_subd_modifier = next((modifier for modifier
                                            in context.active_object.modifiers
                                            if modifier.type == 'SUBSURF'), None)
        if active_object_subd_modifier:
            render_levels_value = active_object_subd_modifier.render_levels
            # select the same
            obj_subd = cls._sub_objects(context=context)
            # deselect all
            cls._deselect_all(context=context)
            for obj in obj_subd:
                subd_modifiers = (modifier for modifier in obj.modifiers
                                  if modifier.type == 'SUBSURF')
                for modifier in subd_modifiers:
                    if modifier.render_levels == render_levels_value:
                        obj.select = True

    @staticmethod
    def _deselect_all(context):
        if context.active_object.mode == 'OBJECT':
            bpy.ops.object.select_all(action='DESELECT')
        elif context.active_object.mode == 'EDIT':
            bpy.ops.mesh.select_all(action='DESELECT')

    @staticmethod
    def _sub_objects(context, selected=False):
        # selected objects with Subdivision Modifier
        if selected:
            return (obj for obj in context.selected_objects
                    if 'SUBSURF' in [modifier.type for modifier in obj.modifiers]
                    )
        else:
            return (obj for obj in context.blend_data.objects
                    if 'SUBSURF' in [modifier.type for modifier in obj.modifiers]
                    )


# --- OPS ----------------------------------------------------


class SUBD_TOOL_OT_store_subd(Operator):
    bl_idname = 'subd_tool.store_subd'
    bl_label = 'Store Subd'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        SubdTool.store_subd(
            context=context
        )
        return {'FINISHED'}


class SUBD_TOOL_OT_view_subd(Operator):
    bl_idname = 'subd_tool.view_subd'
    bl_label = 'View Subd'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        SubdTool.view_subd(
            context=context
        )
        return {'FINISHED'}


class SUBD_TOOL_OT_select_subd(Operator):
    bl_idname = 'subd_tool.select_subd'
    bl_label = 'Select Subd'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        SubdTool.select_subd(
            context=context
        )
        return {'FINISHED'}


# --- UI ----------------------------------------------------


class SUBD_TOOL_PT_panel(Panel):
    bl_idname = 'SUBD_TOOL_PT_panel'
    bl_label = 'Subd Tool'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = '1D'

    def draw(self, context):
        self.layout.operator(
            operator='subd_tool.store_subd'
        )
        self.layout.operator(
            operator='subd_tool.view_subd'
        )
        self.layout.operator(
            operator='subd_tool.select_subd'
        )


# --- REGISTER ----------------------------------------------------


def register():
    register_class(SUBD_TOOL_OT_store_subd)
    register_class(SUBD_TOOL_OT_view_subd)
    register_class(SUBD_TOOL_OT_select_subd)
    register_class(SUBD_TOOL_PT_panel)


def unregister():
    unregister_class(SUBD_TOOL_PT_panel)
    unregister_class(SUBD_TOOL_OT_select_subd)
    unregister_class(SUBD_TOOL_OT_view_subd)
    unregister_class(SUBD_TOOL_OT_store_subd)


if __name__ == '__main__':
    register()
