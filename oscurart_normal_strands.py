import bpy

steps = 20
CUBE = bpy.context.object

mesh = bpy.data.meshes.new("d")
ob = bpy.data.objects.new("objeto",mesh)

VL= []
EL = []

for ver in CUBE.data.vertices:
    for i in range(steps):
        VERNOR = ver.normal        
        VL.append(((VERNOR*i)/(steps-1))+ver.co)
        EL.append(((ver.index+i)+(ver.index*(steps-1)),
            1+(ver.index+i)+(ver.index*(steps-1))))
    EL.pop()    
        
 
mesh.from_pydata(VL,EL,[])    
bpy.context.scene.objects.link(ob)
mesh.update()