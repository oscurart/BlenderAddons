bl_info = {
    "name": "Copy Mirror Constraints",
    "author": "Oscurart",
    "version": (1, 1),
    "blender": (2, 5, 9),
    "api": 40600,
    "location": "Pose > Constraints > Copy Mirror Constraints",
    "description": "Copy Mirror Constraints",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Rigging"}


import bpy

#reemplaza la ultima parte de un string l por r 
def replaceCnsLR (token,cnsType):
    switch = 0
    for left in [".l",".L","_l","_L"]:
        if token.count(left):
            switch = 1  
    if switch:        
        return token.replace(".L",".R").replace(".l",".r").replace("_l","_r").replace("_L","_R")
    else:
        if cnsType == 1:
            return token
        else:
            print("%s havent mirror bone" % (token))

def copy_mirror_constraint(self):
    for bone in bpy.context.selected_pose_bones:                
        osb = bpy.context.object.pose.bones[replaceCnsLR(bone.name,0)] #other side bone
         
        for cns in bone.constraints:  
            oscns = osb.constraints.new(cns.type) #other side constraint  
            for propiedad in  dir(cns):        
                try:
                    setattr(oscns, propiedad, getattr(cns,propiedad))
                    if propiedad == "subtarget":
                        setattr(oscns, propiedad, replaceCnsLR(getattr(cns,propiedad),1))
                except:
                    print(type(getattr(oscns, propiedad)))


class OBJECT_OT_add_object(bpy.types.Operator):
    bl_idname = "pose.copy_constraints_mirror"
    bl_label = "Copy Mirror Constraints"
    bl_description = "Mirror Constraints in PoseBones"
    bl_options = {'REGISTER', 'UNDO'}



    def execute(self, context):

        copy_mirror_constraint(self)

        return {'FINISHED'}


# Registration

def add_object_copy_mirrcns_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Copy Mirror Constraints",
        icon="PLUGIN")


def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.types.VIEW3D_MT_pose_constraints.append(add_object_copy_mirrcns_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.types.VIEW3D_MT_pose_constraints.append(add_object_copy_mirrcns_button)


if __name__ == '__main__':
    register()
