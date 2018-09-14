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


actObj = bpy.context.object
actMesh = actObj.to_mesh(bpy.context.scene, apply_modifiers=True, settings="RENDER", calc_tessface=True, calc_undeformed=True)
selObjs = [ob for ob in bpy.data.objects if ob.type == "MESH"]
selObjs.remove(actObj)


bpy.ops.object.select_all(action="DESELECT")

#objeto activo temporal
actNewObject = bpy.data.objects.new("tempActObj", actMesh)
bpy.context.scene.objects.link(actNewObject)
mat = actObj.matrix_world
for actVert,noVert in zip(actObj.data.vertices,actNewObject.data.vertices):
    noVert.co = mat * actVert.co 
    
bpy.ops.object.mode_set(mode="OBJECT")

#arbol seleccionado
selTree = mathutils.bvhtree.BVHTree.FromObject(actNewObject, bpy.context.scene,deform=True)


for ob in selObjs:
    # creo objeto temporal
    nm = ob.to_mesh(bpy.context.scene, apply_modifiers=True, settings="RENDER", calc_tessface=True, calc_undeformed=True)
    nom = bpy.data.objects.new("tempNActObj", nm)
    bpy.context.scene.objects.link(nom)
    nmat = ob.matrix_world
    for actVert,noVert in zip(ob.data.vertices,nom.data.vertices):
        noVert.co = nmat * actVert.co   
        
    noselTree = mathutils.bvhtree.BVHTree.FromObject(nom, bpy.context.scene,deform=True)
    #calculoArbol
    overlap = mathutils.bvhtree.BVHTree.overlap(selTree,noselTree)    
    actList = list(set([i[0] for i in overlap]))
    for poly in actList:
        actObj.data.polygons[poly].select = True
    selList = list(set([i[1] for i in overlap]))
    for poly in selList:
        ob.data.polygons[poly].select = True    
    if len(overlap) > 0:
        ob.select = 1
        actObj.select = 1    
    
    bpy.data.objects.remove(nom)      
        
        
bpy.data.objects.remove(actNewObject)        

