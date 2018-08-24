import bpy
from mathutils import Vector

mode = bpy.context.object.mode
bpy.ops.object.mode_set(mode="OBJECT")

uvAct = bpy.context.object.data.uv_layers.active


def calcArea(v1,v2,v3):
    v12 = v2 - v1
    v13 = v3 - v1
    v12 = Vector((v12[0],v12[1],0))
    v13 = Vector((v13[0],v13[1],0))
    area = v12.cross(v13).length / 2
    return(area)   
    
total = .0
    
for poly in bpy.context.object.data.polygons:   
    i =0
    pa = .0
    while i != poly.loop_total-2:        
        pa += calcArea(uvAct.data[poly.loop_start].uv,
            uvAct.data[poly.loop_start+1+i].uv,
            uvAct.data[poly.loop_start+2+i].uv)  
        i += 1
    #print(poly.index, pa)
    total += pa

bpy.ops.object.mode_set(mode=mode)

print("Area: %s percent" % (total))        