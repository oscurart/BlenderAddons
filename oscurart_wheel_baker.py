import bpy
from math import sqrt


fs = bpy.context.scene.frame_start
fe = bpy.context.scene.frame_end
ob = bpy.context.active_pose_bone
direccion = bpy.context.object.pose.bones[ob.name+"_vector"]

def get_distance(moveVectorOld,moveVector,frente):
    dif = moveVector - moveVectorOld
    dir = frente - moveVector
    dot = dif.dot(dir)
    i = 1 if dot >= 0 else -1
    return( -dif.magnitude * i)

bpy.context.scene.frame_set(fs)
prev = ob.matrix.copy()
rot = 0

for i in range(fe-fs):
    bpy.context.scene.frame_set(i+1) 
    difRot = get_distance(prev.to_translation(),ob.matrix.to_translation(),direccion.matrix.to_translation()) 
    rot += difRot
    ob.rotation_euler.y = rot
    ob.keyframe_insert("rotation_euler", index=-1, frame=i+1)
    prev = ob.matrix.copy()

