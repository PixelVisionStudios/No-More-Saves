import bpy

def disable_save_confirm(self, context):
    return {'CANCELLED'}

def disable_save():
    bpy.ops.wm.save_mainfile = disable_save_confirm
    bpy.ops.wm.save_mainfile.poll = disable_save_confirm

def enable_save():
    bpy.ops.wm.save_mainfile = bpy.ops.wm.save_mainfile._original
    bpy.ops.wm.save_mainfile.poll = bpy.ops.wm.save_mainfile._original.poll

# Operator to enable/disable save
class DisableSaveOperator(bpy.types.Operator):
    bl_idname = "wm.disable_save"
    bl_label = "Disable Save"
    
    def execute(self, context):
        disable_save()
        return {'FINISHED'}

# Operator to enable/disable save
class EnableSaveOperator(bpy.types.Operator):
    bl_idname = "wm.enable_save"
    bl_label = "Enable Save"
    
    def execute(self, context):
        enable_save()
        return {'FINISHED'}

def register():
    bpy.ops.wm.save_mainfile._original = bpy.ops.wm.save_mainfile
    bpy.ops.wm.save_mainfile = disable_save_confirm
    bpy.ops.wm.save_mainfile.poll = disable_save_confirm

    bpy.utils.register_class(DisableSaveOperator)
    bpy.utils.register_class(EnableSaveOperator)
    
    km = bpy.context.window_manager.keyconfigs.default.keymaps['File']
    km.keymap_items.new(DisableSaveOperator.bl_idname, 'S', 'PRESS', ctrl=True, shift=True)
    km.keymap_items.new(EnableSaveOperator.bl_idname, 'S', 'PRESS', ctrl=True, alt=True)

def unregister():
    bpy.ops.wm.save_mainfile = bpy.ops.wm.save_mainfile._original
    bpy.ops.wm.save_mainfile.poll = bpy.ops.wm.save_mainfile._original.poll

    bpy.utils.unregister_class(DisableSaveOperator)
    bpy.utils.unregister_class(EnableSaveOperator)
    
    km = bpy.context.window_manager.keyconfigs.default.keymaps['File']
    for item in km.keymap_items:
        if item.idname == DisableSaveOperator.bl_idname or item.idname == EnableSaveOperator.bl_idname:
            km.keymap_items.remove(item)

if __name__ == "__main__":
    register()
