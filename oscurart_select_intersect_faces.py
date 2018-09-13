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
import mathutils

bpy.ops.object.mode_set(mode="OBJECT")

#arbol seleccionado
polySel = [poly for poly in bpy.context.object.data.polygons if poly.select]
vertSel = list(set([v for poly in bpy.context.object.data.polygons if poly.select for v in poly.vertices]))
vertSel.sort()
vertIndices = {v:i for i,v in enumerate(vertSel)}
faceIndices = {i:f.index for i,f in enumerate(polySel)}

coVerts = [bpy.context.object.data.vertices[vert].co[:] for vert in vertSel]
polyVerts = [[vertIndices[i] for i in p.vertices] for p in polySel]
selTree = mathutils.bvhtree.BVHTree.FromPolygons(coVerts,polyVerts)

#arbol deseleccionado
nopolySel = [poly for poly in bpy.context.object.data.polygons if not poly.select]
novertSel = list(set([v for poly in bpy.context.object.data.polygons if not poly.select for v in poly.vertices]))
novertSel.sort()
novertIndices = {v:i for i,v in enumerate(novertSel)}
nofaceIndices = {i:f.index for i,f in enumerate(nopolySel)}

nocoVerts = [bpy.context.object.data.vertices[vert].co[:] for vert in novertSel]
nopolyVerts = [[novertIndices[i] for i in p.vertices] for p in nopolySel]
noselTree = mathutils.bvhtree.BVHTree.FromPolygons(nocoVerts,nopolyVerts)

#calculoArbol
overlap = mathutils.bvhtree.BVHTree.overlap(selTree,noselTree)

#forceDeselect    
bpy.ops.object.mode_set(mode="EDIT") 
bpy.ops.mesh.select_all(action="DESELECT")   
bpy.ops.object.mode_set(mode="OBJECT")  

for i in overlap:
    bpy.context.object.data.polygons[nofaceIndices[i[1]]].select = 1        


bpy.ops.object.mode_set(mode="EDIT")

