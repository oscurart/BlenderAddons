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
# Usage: select spot or area light and run. Then load the texture in the lamp node tree.
 
import bpy
 
ob = bpy.context.object

if not ob.data.use_nodes:
    ob.data.use_nodes = True
    
snd = bpy.data.node_groups.new("LampProyector", "ShaderNodeTree")
snc = ob.data.node_tree.nodes.new("ShaderNodeGroup") 
snc.node_tree = snd
 
if ob.data.type == "SPOT":
    coord = snd.nodes.new("ShaderNodeTexCoord")
    mapp = snd.nodes.new("ShaderNodeMapping")
    mapp.vector_type = "TEXTURE"
    tex = snd.nodes.new("ShaderNodeTexImage")
    snd.links.new(mapp.inputs['Vector'], coord.outputs['Normal'])
    #snd.links.new(tex.inputs['Vector'], mapp.outputs['Vector'])
    mapp.driver_add("rotation")
elif ob.data.type == "AREA":
    coord = snd.nodes.new("ShaderNodeNewGeometry")
    mapp = snd.nodes.new("ShaderNodeMapping")
    mapp.vector_type = "TEXTURE"
    tex = snd.nodes.new("ShaderNodeTexImage")
    snd.links.new(mapp.inputs['Vector'], coord.outputs['Incoming'])
    #snd.links.new(tex.inputs['Vector'], mapp.outputs['Vector'])
    mapp.driver_add("rotation")    
 
dict = {0:"X",1:"Y",2:"Z"}
 
for index, axis in dict.items():
    var = snd.animation_data.drivers[index].driver.variables.new()
    snd.animation_data.drivers[index].driver.expression = "var"
    var.type = "TRANSFORMS"
    var.targets[0].id = ob
    var.targets[0].transform_type = "ROT_%s" % (axis)
    
separador = snd.nodes.new("ShaderNodeSeparateXYZ")
combinador = snd.nodes.new("ShaderNodeCombineXYZ")  
offseteador = snd.nodes.new("ShaderNodeMapping")
output = snd.nodes.new("NodeGroupOutput")

divx = snd.nodes.new("ShaderNodeMath")
divx.operation = "DIVIDE"
divy = snd.nodes.new("ShaderNodeMath")
divy.operation = "DIVIDE"

snd.links.new(separador.inputs['Vector'], mapp.outputs['Vector'])
snd.links.new(divx.inputs[0], separador.outputs['X'])
snd.links.new(divy.inputs[0], separador.outputs['Y'])
snd.links.new(divx.inputs[1], separador.outputs['Z'])
snd.links.new(divy.inputs[1], separador.outputs['Z'])
snd.links.new(combinador.inputs['X'],divx.outputs['Value'])
snd.links.new(combinador.inputs['Y'],divy.outputs['Value'])
snd.links.new(combinador.inputs['Z'],separador.outputs['Z'])
snd.links.new(offseteador.inputs['Vector'], combinador.outputs['Vector'])
snd.links.new(tex.inputs['Vector'], offseteador.outputs['Vector'])
snd.links.new(output.inputs[0],tex.outputs['Color'])

offseteador.translation[0] = .5
offseteador.translation[1] = .5

#posiciones
coord.location = (-795,-274)
mapp.location = (-566,-140)
separador.location = (-150,-77)
divx.location = (171,96)
divy.location = (170,-72)
combinador.location = (434,-297)
offseteador.location = (685,-76)
tex.location = (1094,98)
output.location = (1380,96)


