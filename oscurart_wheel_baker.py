# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import bpy
from math import sqrt
from math import atan2

#WheelDirection
wd = True
#freeRotation
freeRot = False

fs = bpy.context.scene.frame_start
fe = bpy.context.scene.frame_end
diameter = .244 #wheelDiameterinUnits

def get_distance(moveVectorOld,moveVector,frente,side):
    dif = moveVector - moveVectorOld
    dir = frente - moveVector
    dot = dif.dot(dir)
    zeroMove = True if dif[0] == 0 and dif[1] == 0 else False
    i = 1 if dot >= 0 else -1
    difFreeRot = dif.copy()
    difFreeRot *= i
    if wd:
        if freeRot:
            return [ side * dif.magnitude * (1/diameter), -atan2(dif[0],dif[1]) ,zeroMove]
        else:
            return [ side * dif.magnitude * i * (1/diameter), -atan2(difFreeRot[0],difFreeRot[1]) ,zeroMove]
    else:
       return [ side * dif.magnitude * i * (1/diameter), -atan2(dif[0],dif[1]) ,zeroMove]    



for ob in bpy.context.selected_pose_bones:
    #directionBone
    direccion = bpy.context.object.pose.bones[ob.name+"_vector"]
    #panBone
    if wd:
        pan = bpy.context.object.pose.bones[ob.name+"_pan"]
    #getSide
    bpy.context.object.data.pose_position = "REST"
    bpy.context.scene.frame_set(fs)
    side = -1 if ob.matrix.to_translation().x > 0 else 1
    bpy.context.object.data.pose_position = "POSE"
    bpy.context.scene.frame_set(fs-1)
    prev = ob.matrix.copy()
    rot = 0 #initialPlace
    directionPrev = 0 #dummy
    #bake
    for i in range(fs,fe+1):
        bpy.context.scene.frame_set(i) 
        difRot = get_distance(prev.to_translation(),
            ob.matrix.to_translation(),
            direccion.matrix.to_translation(),
            side) 
        #tilt    
        rot += difRot[0]
        ob.rotation_euler.y = rot
        ob.keyframe_insert("rotation_euler", index=-1, frame=i)
        print(difRot[2])
        #pan 
        if wd:
            #si no hay movimiento no se mueve
            pan.rotation_euler.y = difRot[1] if difRot[2] == False else directionPrev 
            pan.keyframe_insert("rotation_euler", index=-1, frame=i)  
        
        #adicionales        
        directionPrev = difRot[1] if difRot[2] == False else directionPrev
        prev = ob.matrix.copy()   

print("===================FINISH===================")