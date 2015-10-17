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
# INSTRUCTIONS: Select object for export, and set "save" in action variable, and run. Set action as "load" and hit run for load!

import bpy
import json

action = "save"
 
path = bpy.data.filepath.replace(".blend",".json")  

if action == "save":
    entireData = {}
    for ob in bpy.context.selected_objects:  
        ver = [vert.co[:] for vert in ob.data.vertices]
        edg =  [edge.vertices[:] for edge in ob.data.edges]
        fac =  [face.vertices[:] for face in ob.data.polygons]
        uvs = {ul.name : {i : [loop.uv[0],loop.uv[1]] for i,loop in enumerate(ul.data) } for ul in ob.data.uv_layers }
        entireData[ob.name] = {"vertices" : ver, "edges" : edg, "faces" : fac, "uvs" : uvs} 
    with open(path, "w") as file:
        json.dump(entireData, file, ensure_ascii=False)
        
if action == "load":    
    with open(path, "r") as file:
        ndata = json.load(file)
        for ob in ndata:
            odata = bpy.data.meshes.new(ob+"_mesh")
            object = bpy.data.objects.new(ob,odata)
            odata.from_pydata(ndata[ob]["vertices"],ndata[ob]["edges"],ndata[ob]["faces"])
            odata.update()
            bpy.context.scene.objects.link(object)
            for uv in ndata[ob]["uvs"]:
                newuv = object.data.uv_textures.new(name=uv)
                for i,loop in ndata[ob]["uvs"][uv].items():
                    object.data.uv_layers[uv].data[int(i)].uv = loop
