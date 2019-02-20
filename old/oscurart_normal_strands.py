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
# Usage: make a edge strand from selected object.
# Author: Eugenio Pignataro (Oscurart) www.oscurart.com.ar

import bpy

steps = 20
OBJECT = bpy.context.object

mesh = bpy.data.meshes.new("mesh")
ob = bpy.data.objects.new("objeto",mesh)

VL= []
EL = []

for ver in OBJECT.data.vertices:
    for i in range(steps):
        VERNOR = ver.normal        
        VL.append(((VERNOR*i)/(steps-1))+ver.co)
        EL.append(((ver.index+i)+(ver.index*(steps-1)),
            1+(ver.index+i)+(ver.index*(steps-1))))
    EL.pop()            
 
mesh.from_pydata(VL,EL,[])    
bpy.context.scene.objects.link(ob)
mesh.update()