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
# Usage: set the frame in the initial state and run. Then scrub the timeline.
# Author: Eugenio Pignataro (Oscurart) www.oscurart.com.ar



import bpy

hd = { particle: [hk.co[:] for hk in particle.hair_keys] for i,particle in enumerate(bpy.context.object.particle_systems.active.particles)}

bpy.context.object.particle_systems.active.use_hair_dynamics = False
bpy.context.scene.frame_set(frame=1)

for particle,list in hd.items():
    for hk,hkr in zip(list,particle.hair_keys):
        hkr.co = hk

     