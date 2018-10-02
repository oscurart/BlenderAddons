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
import bmesh


#variables
parts = 2


me = bpy.data.meshes.new("MergeObject")

indexSuma = 0
uvLayerSuma = 0
totalVertices = []
totalFaces = []
uvLayers = {}
quadrantex = 0
quadrantey = 0

for ob in bpy.context.selected_objects:
    obMatrix = ob.matrix_world    
    for vert in ob.data.vertices:
        totalVertices.append(obMatrix * vert.co)        
    for face in ob.data.polygons:
        facetemp = []
        for indice in face.vertices[:]:
            facetemp.append(indice+indexSuma)
        totalFaces.append(facetemp)    
    faces = [face.vertices[:] for face in ob.data.polygons]
    for i , uvl in enumerate(ob.data.uv_layers[0].data):
        quad = uvl.uv * (1/parts)
        quad[0] += ((1/parts)*quadrantex)
        quad[1] += ((1/parts)*quadrantey)
        uvLayers[i+uvLayerSuma] = quad
    indexSuma += len(ob.data.vertices)
    uvLayerSuma += len(ob.data.uv_layers[0].data)
    quadrantex += 1
    if quadrantex == parts:
        quadrantex = 0
        quadrantey += 1
            
me.from_pydata(totalVertices,[],totalFaces)
uv = me.uv_textures.new(name="UVMap")

for i,uv in enumerate(me.uv_layers[0].data):
    uv.uv = uvLayers[i]
    
ob = bpy.data.objects.new("MergeObject", me)
bpy.context.scene.objects.link(ob)


bpy.ops.object.select_all(action="DESELECT")
ob.select = True
bpy.context.scene.objects.active = ob
bpy.ops.object.mode_set(mode="EDIT")
