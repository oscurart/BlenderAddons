import bpy
import json

import json
 
ob = bpy.context.object
 
ver = [vert.co[:] for vert in ob.data.vertices]
edg =  [edge.vertices[:] for edge in ob.data.edges]
fac =  [face.vertices[:] for face in ob.data.polygons]

data = {"vertices" : ver, "edges" : edg, "faces" : fac}

with open("C:/Users/Admin/Desktop/TODO_PRUEBA/JSON_MSH.json", "w") as file:
    json.dump(data, file, ensure_ascii=False)
    
with open("C:/Users/Admin/Desktop/TODO_PRUEBA/JSON_MSH.json", "r") as file:
    ndata = json.load(file)
     

odata = bpy.data.meshes.new("mesh")
object = bpy.data.objects.new("objetito",odata)
odata.from_pydata(ndata["vertices"],ndata["edges"],ndata["faces"])
bpy.context.scene.objects.link(object)