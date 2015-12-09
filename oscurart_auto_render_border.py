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
# USAGE: Run script!


import bpy
from bpy.app.handlers import persistent
from bpy_extras.object_utils import world_to_camera_view

def autoCrop(dummy):
    bpy.context.scene.render.use_border = True
    x, y = [], []
    for ob in bpy.data.objects:
        if ob.type == "MESH" and ob.is_visible(bpy.context.scene):
            nmesh = ob.to_mesh(bpy.context.scene,True,"RENDER")
            for vert in nmesh.vertices:
                gl = ob.matrix_world * vert.co
                cc = world_to_camera_view(bpy.context.scene, bpy.context.scene.camera, gl)
                x.append(cc[0])
                y.append(cc[1])   
            bpy.data.meshes.remove(nmesh)             
    x.sort()
    y.sort()
    bpy.context.scene.render.border_min_x = x[0]
    bpy.context.scene.render.border_max_x = x[-1]
    bpy.context.scene.render.border_min_y = y[0]
    bpy.context.scene.render.border_max_y = y[-1]

bpy.app.handlers.render_init.append(autoCrop)
