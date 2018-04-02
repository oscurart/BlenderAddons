# Select the Low Res mesh and run. You need have a Cage set in render bake options

import bpy

me = bpy.data.meshes.new("mesh")
ob = bpy.data.objects.new("object", me)

lr = bpy.context.object
cage = bpy.data.objects[bpy.context.scene.render.bake.cage_object]

verts = []

for v in cage.data.vertices:
    verts.append(v.co + cage.matrix_world.to_translation()) 

for v in lr.data.vertices :
    verts.append(v.co + lr.matrix_world.to_translation()) 
    
lenVert = len(lr.data.vertices)    
edges = [(i,i+lenVert)for i in range(0,len(lr.data.vertices))]


me.from_pydata(verts, edges, [])

bpy.context.scene.objects.link(ob)

