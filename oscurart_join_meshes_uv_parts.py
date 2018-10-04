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
quadsUp = 1 #zero for non up


me = bpy.data.meshes.new("MergeObject")

indexSuma = 0
faceSuma = 0
uvLayerSuma = 0
totalVertices = []
totalFaces = []
uvLayers = {}
uvLayersOrig = {}
quadrantex = 0
quadrantey = 0
smooth = {}
materials = {}
relObjVerts = {}

for iob, ob in enumerate(bpy.context.selected_objects):
    relObjVerts[ob.name] = []
    #materials
    materials[iob] = ob.active_material.name 
    #matrix del objeto para multiplicar       
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
        #smooth material
        smooth[face.index+faceSuma] = [face.use_smooth,iob]
    faces = [face.vertices[:] for face in ob.data.polygons]
    #uv data
    for i , uvl in enumerate(ob.data.uv_layers[0].data):
        #offseteado
        quad = uvl.uv * (1/parts)
        quad[0] += ((1/parts)*quadrantex)
        quad[1] += ((1/parts)*quadrantey)
        uvLayers[i+uvLayerSuma] = quad
        #original
        uvLayersOrig[i+uvLayerSuma] = uvl.uv     
        #guardo los objetos y vertices relativos al objeto fuente
        relObjVerts[ob.name].append([i,i+uvLayerSuma])
    #incremental variables    
    indexSuma += len(ob.data.vertices)
    faceSuma += len(ob.data.polygons)
    uvLayerSuma += len(ob.data.uv_layers[0].data)
    quadrantex += 1
    if quadrantex == parts:
        quadrantex = 0
        quadrantey += quadsUp

#set mesh           
me.from_pydata(totalVertices,[],totalFaces)
uv = me.uv_textures.new(name="UVMap")
uvorig = me.uv_textures.new(name="UVMapOrig")

#set uvs
for i,uvt in enumerate(me.uv_layers["UVMap"].data):
    uvt.uv = uvLayers[i]

#set original uv
for i,uvo in enumerate(me.uv_layers["UVMapOrig"].data):
    uvo.uv = uvLayersOrig[i]

#link mesh    
ob = bpy.data.objects.new("MergeObject", me)
bpy.context.scene.objects.link(ob)

#material slots
for imat,mat in materials.items():
    ob.data.materials.append(bpy.data.materials[mat])

#set smooth and mat
for i in smooth:
    me.polygons[i].use_smooth = smooth[i][0]  
    me.polygons[i].material_index = smooth[i][1]

#creo el uv atlas en los objetos anteriores
for origOb,data in relObjVerts.items():
    try:
        bpy.context.object.data.uv_layers["Atlas"]
    except:    
        bpy.data.objects[origOb].data.uv_textures.new(name="Atlas")
    for uvData in data:
        bpy.data.objects[origOb].data.uv_layers["Atlas"].data[uvData[0]].uv = me.uv_layers["UVMap"].data[uvData[1]].uv

#active object
bpy.ops.object.select_all(action="DESELECT")
ob.select = True
bpy.context.scene.objects.active = ob
bpy.ops.object.mode_set(mode="EDIT")
me.uv_textures['UVMapOrig'].active_render =1


print("-----------------------------------")
