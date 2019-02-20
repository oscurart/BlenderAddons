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
# Uso Instrucciones: Crea un mesh con vertices a partir de un sistema de particulas. Seleccionar el objeto con las particulas y correr.
# Make a mesh object from selected particle system. Select the particle system object and run.


import bpy

ME = bpy.data.meshes.new("me")
OB = bpy.data.objects.new("ob",ME)
PL = [i.location for i in bpy.context.object.particle_systems[0].particles ] #if i.alive_state == "ALIVE" and i.is_exist
ME.from_pydata(PL,[],[])
bpy.context.scene.objects.link(OB)



