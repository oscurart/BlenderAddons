import bpy



ARMATURE=bpy.context.active_object

for hueso in ARMATURE.pose.bones:
    if hueso.rotation_mode != 'XYZ':
        hueso.rotation_mode = 'XYZ'

print ("LISTO")


