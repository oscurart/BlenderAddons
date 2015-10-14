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

if bpy.context.scene.render.engine == 'CYCLES':
    # check world use nodes
    if not bpy.context.scene.world.use_nodes:
        bpy.context.scene.world.use_nodes = True 
    # check selection and lamp
    if bpy.context.object != None and bpy.context.object.type == 'LAMP':
        if bpy.context.object.data.type == 'SUN':           
            lampob = bpy.context.object
        else:
            lampob = bpy.context.object
            bpy.context.object.data.type = 'SUN'    
    else:
        lamp = bpy.data.lamps.new("Sun", "SUN")
        lampob = bpy.data.objects.new("SunRig", lamp)  
        bpy.context.scene.objects.link(lampob)                    
    # setting shader
    shader = [node for node in bpy.context.scene.world.node_tree.nodes[:] if node.type == "TEX_SKY"]
    if len(shader) > 0:
        shader = shader[0]
    else:
        shader = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexSky")
        bgnode = [node for node in bpy.context.scene.world.node_tree.nodes[:] if node.type == "BACKGROUND"][0]
        bpy.context.scene.world.node_tree.links.new(shader.outputs['Color'], bgnode.inputs['Color'])        
    dr = shader.driver_add("sun_direction")
    # set drivers
    # X
    dr[0].driver.expression = 'var'
    var = dr[0].driver.variables.new()
    var.type = 'SINGLE_PROP'
    var.targets[0].id = lampob
    var.targets[0].data_path = 'matrix_world[2][0]'
    # Y
    dr[1].driver.expression = 'var'
    var = dr[1].driver.variables.new()
    var.type = 'SINGLE_PROP'
    var.targets[0].id = lampob
    var.targets[0].data_path = 'matrix_world[2][1]'    
    # Y
    dr[2].driver.expression = 'var'
    var = dr[2].driver.variables.new()
    var.type = 'SINGLE_PROP'
    var.targets[0].id = lampob
    var.targets[0].data_path = 'matrix_world[2][2]'                     
else:
    print("Please change your render engine to Cycles!")    
     