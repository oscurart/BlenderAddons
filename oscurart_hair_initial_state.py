"""
Author: Eugenio Pignataro Oscurart
Site: www.oscurart.com.ar
Email: info@oscurart.com.ar
Usage: set the frame in the initial state and rund. Then scrub the timeline.

"""


import bpy

hd = { particle: [hk.co[:] for hk in particle.hair_keys] for i,particle in enumerate(bpy.context.object.particle_systems.active.particles)}

bpy.context.object.particle_systems.active.use_hair_dynamics = False
bpy.context.scene.frame_set(frame=1)

for particle,list in hd.items():
    for hk,hkr in zip(list,particle.hair_keys):
        hkr.co = hk

     