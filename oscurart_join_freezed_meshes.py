"""
Este Script hace un merge de los objetos seleccionados en un objeto nuevo llamado joinMesh
"""


import bpy
import bmesh

freezeMeshes = []

for ob in bpy.context.selected_objects:
    freezeMeshes.append(ob.to_mesh(bpy.context.scene, True, "RENDER",True, False) )


bm = bmesh.new()

for mesh in freezeMeshes:
    bm.from_mesh( mesh )

joinMesh = bpy.data.meshes.new( "joinMesh" )
bm.to_mesh( joinMesh )

joinObject = bpy.data.objects.new( "joinMesh", joinMesh )
bpy.context.scene.objects.link( joinObject )