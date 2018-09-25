# Select the Low Res mesh and run. You need have a Cage set in render bake options

import bpy

SUBDIVISIONS = 2
inner = .95 #1
outer = 1.05 #1



me = bpy.data.meshes.new("mesh")
ob = bpy.data.objects.new("object", me)

lr = bpy.context.object
cage = bpy.data.objects[bpy.context.scene.render.bake.cage_object]

ss = lr.modifiers.new("TMP","SUBSURF")
ss.render_levels = SUBDIVISIONS
ss.subdivision_type = "SIMPLE"
nlr = lr.to_mesh(bpy.context.scene, True, "RENDER")
lr.modifiers.remove(ss)

ss = cage.modifiers.new("TMP","SUBSURF")
ss.render_levels = SUBDIVISIONS
ss.subdivision_type = "SIMPLE"
ncage = cage.to_mesh(bpy.context.scene, True, "RENDER")
cage.modifiers.remove(ss)


verts = []

for v in ncage.vertices:    
    verts.append(cage.matrix_world * v.co * outer) 

for v in nlr.vertices :
    verts.append(lr.matrix_world * v.co * inner) 
    
lenVert = len(nlr.vertices)    
edges = [(i,i+lenVert)for i in range(0,len(nlr.vertices))]


me.from_pydata(verts, edges, [])

bpy.context.scene.objects.link(ob)

del(nlr)
del(ncage)
