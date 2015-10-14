import bpy

ME = bpy.data.meshes.new("me")
OB = bpy.data.objects.new("ob",ME)
PL = [i.location for i in bpy.context.object.particle_systems[0].particles ] #if i.alive_state == "ALIVE" and i.is_exist
ME.from_pydata(PL,[],[])
bpy.context.scene.objects.link(OB)



