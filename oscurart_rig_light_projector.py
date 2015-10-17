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

# Author: Eugenio Pignataro Oscurart
# Mail: Info@oscurart.com.ar
# Website: www.oscurart.com.ar

 
import bpy
 
ob = bpy.context.object
 
if not ob.data.use_nodes:
    ob.data.use_nodes = True
 
if ob.data.type == "SPOT":
    coord = ob.data.node_tree.nodes.new("ShaderNodeTexCoord")
    mapp = ob.data.node_tree.nodes.new("ShaderNodeMapping")
    mapp.vector_type = "TEXTURE"
    tex = ob.data.node_tree.nodes.new("ShaderNodeTexImage")
    ob.data.node_tree.links.new(mapp.inputs['Vector'], coord.outputs['Normal'])
    ob.data.node_tree.links.new(tex.inputs['Vector'], mapp.outputs['Vector'])
    mapp.driver_add("rotation")
elif ob.data.type == "AREA":
    coord = ob.data.node_tree.nodes.new("ShaderNodeNewGeometry")
    mapp = ob.data.node_tree.nodes.new("ShaderNodeMapping")
    mapp.vector_type = "TEXTURE"
    tex = ob.data.node_tree.nodes.new("ShaderNodeTexImage")
    ob.data.node_tree.links.new(mapp.inputs['Vector'], coord.outputs['Incoming'])
    ob.data.node_tree.links.new(tex.inputs['Vector'], mapp.outputs['Vector'])
    mapp.driver_add("rotation")    
 
dict = {0:"X",1:"Y",2:"Z"}
 
for index, axis in dict.items():
    var = ob.data.node_tree.animation_data.drivers[index].driver.variables.new()
    ob.data.node_tree.animation_data.drivers[index].driver.expression = "var"
    var.type = "TRANSFORMS"
    var.targets[0].id = ob
    var.targets[0].transform_type = "ROT_%s" % (axis)