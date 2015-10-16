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
# USAGE: Enable compositor nodes and run script!

import bpy


sc = bpy.context.scene
groupdata = bpy.data.node_groups.new("DECOMPOSE","CompositorNodeTree")
gr = sc.node_tree.nodes.new("CompositorNodeGroup")
gr.node_tree = groupdata
input = gr.node_tree.nodes.new("NodeGroupInput")
output = gr.node_tree.nodes.new("NodeGroupOutput")

# emission
addE = gr.node_tree.nodes.new("CompositorNodeMixRGB")
addE.blend_type = "ADD"
gr.node_tree.links.new(input.outputs[''],addE.inputs[2])
groupdata.inputs[0].name = "Emit"

# suma diffuses
addD = gr.node_tree.nodes.new("CompositorNodeMixRGB")
multD = gr.node_tree.nodes.new("CompositorNodeMixRGB")
addD.blend_type = "ADD"
multD.blend_type = "MULTIPLY"
gr.node_tree.links.new(input.outputs[''],addD.inputs[1])
gr.node_tree.links.new(input.outputs[''],addD.inputs[2])
gr.node_tree.links.new(input.outputs[''],multD.inputs[2])
gr.node_tree.links.new(addD.outputs[0],multD.inputs[1])
groupdata.inputs[1].name = "Diffuse Direct"
groupdata.inputs[2].name = "Diffuse Indirect"
groupdata.inputs[3].name = "Diffuse Color"

# suma Glossy
addG = gr.node_tree.nodes.new("CompositorNodeMixRGB")
multG = gr.node_tree.nodes.new("CompositorNodeMixRGB")
addG.blend_type = "ADD"
multG.blend_type = "MULTIPLY"
gr.node_tree.links.new(input.outputs[''],addG.inputs[1])
gr.node_tree.links.new(input.outputs[''],addG.inputs[2])
gr.node_tree.links.new(input.outputs[''],multG.inputs[2])
gr.node_tree.links.new(addG.outputs[0],multG.inputs[1])
groupdata.inputs[4].name = "Glossy Direct"
groupdata.inputs[5].name = "Glossy Indirect"
groupdata.inputs[6].name = "Glossy Color"

# suma Transmission
addT = gr.node_tree.nodes.new("CompositorNodeMixRGB")
multT = gr.node_tree.nodes.new("CompositorNodeMixRGB")
addT.blend_type = "ADD"
multT.blend_type = "MULTIPLY"
gr.node_tree.links.new(input.outputs[''],addT.inputs[1])
gr.node_tree.links.new(input.outputs[''],addT.inputs[2])
gr.node_tree.links.new(input.outputs[''],multT.inputs[2])
gr.node_tree.links.new(addT.outputs[0],multT.inputs[1])
groupdata.inputs[7].name = "Transmission Direct"
groupdata.inputs[8].name = "Transmission Indirect"
groupdata.inputs[9].name = "Transmission Color"


# suma SSS
addS = gr.node_tree.nodes.new("CompositorNodeMixRGB")
multS = gr.node_tree.nodes.new("CompositorNodeMixRGB")
addS.blend_type = "ADD"
multS.blend_type = "MULTIPLY"
gr.node_tree.links.new(input.outputs[''],addS.inputs[1])
gr.node_tree.links.new(input.outputs[''],addS.inputs[2])
gr.node_tree.links.new(input.outputs[''],multS.inputs[2])
gr.node_tree.links.new(addS.outputs[0],multS.inputs[1])
groupdata.inputs[10].name = "SSS Direct"
groupdata.inputs[11].name = "SSS Indirect"
groupdata.inputs[12].name = "SSS Color"



addDG = gr.node_tree.nodes.new("CompositorNodeMixRGB")
addDGT = gr.node_tree.nodes.new("CompositorNodeMixRGB")
addDGTS = gr.node_tree.nodes.new("CompositorNodeMixRGB")
addDG.blend_type = "ADD"
addDGT.blend_type = "ADD"
addDGTS.blend_type = "ADD"
gr.node_tree.links.new(multG.outputs[0],addDG.inputs[2])
gr.node_tree.links.new(multD.outputs[0],addDG.inputs[1])
gr.node_tree.links.new(multT.outputs[0],addDGT.inputs[2])
gr.node_tree.links.new(addDG.outputs[0],addDGT.inputs[1])
gr.node_tree.links.new(addDGT.outputs[0],addDGTS.inputs[1])
gr.node_tree.links.new(multS.outputs[0],addDGTS.inputs[2])

# emission links
gr.node_tree.links.new(addDGTS.outputs[0],addE.inputs[1])


# outputs
gr.node_tree.links.new(addE.outputs[0],output.inputs[''])
gr.node_tree.links.new(multD.outputs[0],output.inputs[''])
gr.node_tree.links.new(multG.outputs[0],output.inputs[''])
gr.node_tree.links.new(multT.outputs[0],output.inputs[''])
gr.node_tree.links.new(multS.outputs[0],output.inputs[''])
groupdata.outputs[0].name = "Combined"
groupdata.outputs[1].name = "Diffuse"
groupdata.outputs[2].name = "Glossy"
groupdata.outputs[3].name = "Transmission"
groupdata.outputs[4].name = "Scatter"


