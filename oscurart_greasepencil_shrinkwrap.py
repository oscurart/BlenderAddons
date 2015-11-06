import bpy
import bmesh
from mathutils.geometry import intersect_line_line

mesh = bpy.context.object
bm = bmesh.from_edit_mesh(mesh.data)

for vertice in bm.verts:
    if vertice.select:
        imen = -1000
        imay = 1000
        punto = vertice.co[:]
        jj= [point.co for point in bpy.context.object.grease_pencil.layers.active.frames[0].strokes[0].points]
        for point in bpy.data.grease_pencil[0].layers.active.frames[0].strokes[0].points:
            if point.co.x < punto[0] and point.co.x > imen:
                imen = point.co.x
                men = point.co
            if point.co.x > punto[0] and point.co.x < imay:
                imay = point.co.x
                may = point.co                          
        vertice.co = (vertice.co.x,vertice.co.y,intersect_line_line(men,may,punto,(punto[0],punto[1],punto[2]+1))[0][2])
        
bmesh.update_edit_mesh(mesh.data)
bm.free() 