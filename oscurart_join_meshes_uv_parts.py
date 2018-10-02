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
partsY = 1 #zero for non up


me = bpy.data.meshes.new("MergeObject")

indexSuma = 0
faceSuma = 0
uvLayerSuma = 0
totalVertices = []
totalFaces = []
uvLayers = {}
quadrantex = 0
quadrantey = 0
smooth = {}

for ob in bpy.context.selected_objects:
    obMatrix = ob.matrix_world    
    #vert position
    for vert in ob.data.vertices:
        totalVertices.append(obMatrix * vert.co)   
    #face data collect         
    for face in ob.data.polygons:
        facetemp = []
        for indice in face.vertices[:]:
            facetemp.append(indice+indexSuma)
        totalFaces.append(facetemp)  
        smooth[face.index+faceSuma] = face.use_smooth
    faces = [face.vertices[:] for face in ob.data.polygons]
    #uv data
    for i , uvl in enumerate(ob.data.uv_layers[0].data):
        quad = uvl.uv * (1/parts)
        quad[0] += ((1/parts)*quadrantex)
        quad[1] += ((1/parts)*quadrantey)
        uvLayers[i+uvLayerSuma] = quad
    #incremental variables    
    indexSuma += len(ob.data.vertices)
    faceSuma += len(ob.data.polygons)
    uvLayerSuma += len(ob.data.uv_layers[0].data)
    quadrantex += 1
    if quadrantex == parts:
        quadrantex = 0
        quadrantey += partsY

#set mesh           
me.from_pydata(totalVertices,[],totalFaces)
uv = me.uv_textures.new(name="UVMap")

#set uvs
for i,uv in enumerate(me.uv_layers[0].data):
    uv.uv = uvLayers[i]
 
#set smooth 
for i in smooth:
    me.polygons[i].use_smooth = smooth[i]
    print(smooth[i])

#link mesh    
ob = bpy.data.objects.new("MergeObject", me)
bpy.context.scene.objects.link(ob)

#active object
bpy.ops.object.select_all(action="DESELECT")
ob.select = True
bpy.context.scene.objects.active = ob
bpy.ops.object.mode_set(mode="EDIT")
