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
# Usage: create a new object from selected object with shapes.
# Author: Eugenio Pignataro (Oscurart) www.oscurart.com.ar




import bpy


for obs in bpy.context.selected_objects:
    original = obs
    originalBasis = original.data.shape_keys.key_blocks[0].name
    kbl = []

    for kb in original.data.shape_keys.key_blocks:
        for kbi in original.data.shape_keys.key_blocks:
            kbi.value = 0     
        kb.value = 1      
        var = original.to_mesh(bpy.context.scene, True, "RENDER")
        var.name = kb.name     
        kbl.append(kb.name)    
                    
    ob = bpy.data.objects.new(original.name+"_COMPUESTO", bpy.data.meshes[originalBasis] )    
    bpy.context.scene.objects.link(ob)

    for kb in kbl:
        ob.shape_key_add(name=kb, from_mix=True)
        for source, target in zip(bpy.data.meshes[kb].vertices, ob.data.shape_keys.key_blocks[kb].data):
            target.co = source.co    

