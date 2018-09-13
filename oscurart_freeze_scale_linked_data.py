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
# USAGE: Select object and run. This script freeze scale in linked mesh data.


import bpy


for ob in bpy.context.selected_objects:
    
    odata = bpy.context.object.data
    
    for vert in ob.data.vertices:
        vert.co[0] *= ob.scale[0] 
        vert.co[1] *= ob.scale[1]
        vert.co[2] *= ob.scale[2]
        
    ob.scale = (1,1,1)   
    
    for lob in bpy.data.objects:
        if lob.data == odata:
            lob.scale = (1,1,1)