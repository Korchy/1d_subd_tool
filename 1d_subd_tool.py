# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/1d_subd_tool
#
# Version history:
#   2022.03.20 - 1.0.0. - initial release
#   2022.03.20 - 1.0.1. - некоторые изменения в названиях,
#       - добавлено description в операторы,
#       - store_subd если модификатор Subdivision Surface отсутствует на объекте - создается
#           новый с View = 0, Render = 0
#       - изменено расположение кнопок в панели
#       - вывод сообщения в INFO
#   2022.03.20 - 1.0.2. - добавление 1D префикса в название и имя файла
#       - изменен формат строки вывода в INFO
#       - Review - Restore
#       - добавлена принудительная перерисовка окон после вызова функций

import bpy
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class


bl_info = {
    'name': '1D SUBD_TOOL',
    'category': 'All',
    'author': 'Nikita Akimov',
    'version': (1, 0, 2),
    'blender': (2, 79, 0),
    'location': 'The 3D_View window - T-panel - the 1D tab',
    'wiki_url': 'https://github.com/Korchy/1d_subd_tool',
    'tracker_url': 'https://github.com/Korchy/1d_subd_tool',
    'description': 'Tool for work with objects with the Subdivision Surface modifier'
}


class SubdTool:

    @classmethod
    def store_subd(cls, context):
        # View to Render in Subdivision Modifier for selected objects
        message = 'Subd objects stored: '
        for obj in context.selected_objects:
            if 'SUBSURF' not in (modifier.type for modifier in obj.modifiers):
                modifier = obj.modifiers.new(
                    name='Subsurf',
                    type='SUBSURF'
                )
                modifier.render_levels = 0
                modifier.levels = 0
            else:
                # View to Render
                modifiers = (modifier for modifier in obj.modifiers
                             if modifier.type == 'SUBSURF')
                for modifier in modifiers:
                    modifier.render_levels = modifier.levels
        message += SubdTool.info_subd(context=context, selected=True)
        # force redraw areas
        cls._redraw_areas(context=context)
        return message

    @classmethod
    def view_subd(cls, context):
        # Render to View in Subdivision Modifier for selected objects
        message = 'Subd objects stored: '
        for obj in context.selected_objects:
            if 'SUBSURF' not in (modifier.type for modifier in obj.modifiers):
                modifier = obj.modifiers.new(
                    name='Subsurf',
                    type='SUBSURF'
                )
                modifier.render_levels = 0
                modifier.levels = 0
            else:
                # Render to View
                modifiers = (modifier for modifier in obj.modifiers
                             if modifier.type == 'SUBSURF')
                for modifier in modifiers:
                    modifier.levels = modifier.render_levels
        message += SubdTool.info_subd(context=context, selected=True)
        # force redraw areas
        cls._redraw_areas(context=context)
        return message

    @classmethod
    def select_subd(cls, context):
        # select objects with Render = Render in active object
        render_levels_value = 0
        # subdivision value from active object
        active_object_subd_modifier = next((modifier for modifier
                                            in context.active_object.modifiers
                                            if modifier.type == 'SUBSURF'), None)
        if active_object_subd_modifier:
            # active object has Subdivision modifier - select with same render_level
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
        else:
            # no Subdivision modifier on active object - select same
            cls._deselect_all(context=context)
            obj_no_subd = (obj for obj in context.blend_data.objects
                           if 'SUBSURF' not in (modifier.type for modifier in obj.modifiers))
            for obj in obj_no_subd:
                obj.select = True
        # force redraw areas
        cls._redraw_areas(context=context)
        return 'S' + str(render_levels_value) + \
               ' ' + str(len(context.selected_objects)) + ' objects selected'

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

    @classmethod
    def info_subd(cls, context, selected):
        # return count of objects with Subdivision Surface modifiers by render_level value
        obj_subd = cls._sub_objects(
            context=context,
            selected=selected
        )
        levels = {}
        modifiers = (modifier for obj in obj_subd for modifier in obj.modifiers
                     if modifier.type == 'SUBSURF')
        for modifier in modifiers:
            if 'S' + str(modifier.render_levels) not in levels:
                levels['S' + str(modifier.render_levels)] = 1
            else:
                levels['S' + str(modifier.render_levels)] += 1
        levels_str = ''
        for key in sorted(levels):
            # levels_str += '%s = %s ' % (key, levels[key])
            levels_str += '%s/%s ' % (levels[key], key)
        return levels_str

    @staticmethod
    def _redraw_areas(context):
        # refresh screen areas
        if context.screen:
            for area in context.screen.areas:
                area.tag_redraw()

# --- OPS ----------------------------------------------------


class SUBD_TOOL_OT_store_subd(Operator):
    bl_idname = 'subd_tool.store_subd'
    bl_label = 'Store Subd'
    bl_description = 'Copy View to Render value for Subd modifier of every ' \
                     'selected object or set zero Subd if is not set'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        message = SubdTool.store_subd(
            context=context
        )
        self.report(
            type={'INFO'},
            message=message
        )
        return {'FINISHED'}


class SUBD_TOOL_OT_view_subd(Operator):
    bl_idname = 'subd_tool.view_subd'
    bl_label = 'Restore Subd'
    bl_description = 'Copy Render to View value for Subd modifier of every ' \
                     'selected object or set zero Subd if is not set'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        message = SubdTool.view_subd(
            context=context
        )
        self.report(
            type={'INFO'},
            message=message
        )
        return {'FINISHED'}


class SUBD_TOOL_OT_select_subd(Operator):
    bl_idname = 'subd_tool.select_subd'
    bl_label = 'Select same subd'
    bl_description = 'Select objects with the same Render subd value'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        message = SubdTool.select_subd(
            context=context
        )
        self.report(
            type={'INFO'},
            message=message
        )
        return {'FINISHED'}


# --- UI ----------------------------------------------------


class SUBD_TOOL_PT_panel(Panel):
    bl_idname = 'SUBD_TOOL_PT_panel'
    bl_label = '1D Subd Tool'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = '1D'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator(
            operator='subd_tool.store_subd'
        )
        row.operator(
            operator='subd_tool.view_subd'
        )
        layout.operator(
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
