# Compensa el tamanio de imagen al modificar el lente de la camara.


bl_info = {
    "name": "Resize Render Resolution",
    "author": "Oscurart",
    "version": (1, 0),
    "blender": (2, 66, 0),
    "location": "Search > Resize Resolution by Camera Angle",
    "description": "Resize render dimension by camera angle.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Render"}


import bpy
import math

C = bpy.context

def defResizeResolution(context, anguloInicio, anguloPrimero, resx, resy):
        
    # calcula valores
    anguloActual= math.degrees(anguloInicio/ 2)
    proportionxy = resx  / resy
    
    opuesto = resx / 2
    adyacente = opuesto / math.tan(anguloInicio / 2)
    newx = (adyacente * math.tan(math.radians(anguloPrimero/2))) * 2

    # setea valores
    C.scene.render.resolution_x = newx
    C.scene.render.resolution_y = newx / proportionxy
    C.scene.camera.data.angle = math.radians(anguloPrimero)


class ResizeResolution(bpy.types.Operator):
    bl_idname = "scene.resize_resolution"
    bl_label = "Resize Resolution by Camera Angle"
    bl_options = {"REGISTER", "UNDO"}
    
    anguloPrimero = bpy.props.FloatProperty(name="Field of View", default=math.degrees(bpy.context.scene.camera.data.angle), min=.01 )
        
    def execute(self, context):
        anguloInicio = bpy.context.scene.camera.data.angle    
        resx = C.scene.render.resolution_x
        resy = C.scene.render.resolution_y
        defResizeResolution(context, anguloInicio, self.anguloPrimero, resx, resy)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ResizeResolution)


def unregister():
    bpy.utils.unregister_class(ResizeResolution)


if __name__ == "__main__":
    register()
