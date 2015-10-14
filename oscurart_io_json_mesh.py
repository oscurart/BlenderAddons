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

# AUTHOR: Eugenio Pignataro (Oscurart) www.oscurart.com.ar


import bpy
import json

import json
 
ob = bpy.context.object
 
ver = [vert.co[:] for vert in ob.data.vertices]
edg =  [edge.vertices[:] for edge in ob.data.edges]
fac =  [face.vertices[:] for face in ob.data.polygons]

data = {"vertices" : ver, "edges" : edg, "faces" : fac}

with open("C:/Users/Admin/Desktop/TODO_PRUEBA/JSON_MSH.json", "w") as file:
    json.dump(data, file, ensure_ascii=False)
    
with open("C:/Users/Admin/Desktop/TODO_PRUEBA/JSON_MSH.json", "r") as file:
    ndata = json.load(file)
     

odata = bpy.data.meshes.new("mesh")
object = bpy.data.objects.new("objetito",odata)
odata.from_pydata(ndata["vertices"],ndata["edges"],ndata["faces"])
bpy.context.scene.objects.link(object)