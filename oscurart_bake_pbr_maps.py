import bpy
import os


size = 512
selected_to_active= False


channels = {"metallic":["ME","GLOSSY"],
    "normal":["NM","NORMAL"],
    "emit":["EM","EMIT"],
    "roughness":["RO","ROUGHNESS"],
    "opacity":["OP","TRANSMISSION"],
    "albedo":["AT","DIFFUSE"]}


#set bake options
bpy.context.scene.render.bake_type = "TEXTURE"
bpy.context.scene.render.bake.use_pass_direct = 0
bpy.context.scene.render.bake.use_pass_indirect = 0
bpy.context.scene.render.bake.use_pass_color = 1
bpy.context.scene.render.bake.use_selected_to_active = selected_to_active


object = bpy.context.object
metalstate = 0 #variable que indica que ya se desmetalizo.

#lista de materiales originales y copias
ms = [mat.material for mat in object.material_slots]
mscopy = []

#sumo materiales copia y reemplazo slots
ims = 0
for mat in ms:
    mc = mat.copy()
    mscopy.append(mc)
    object.material_slots[ims].material = mc
    ims += 1

#desmetalizar
def desmetalizar(activeMat):
    global mscopy
    for mat in mscopy:
        for link in mat.node_tree.links:
            if link.to_socket.name == "Metallic":
                mat.node_tree.links.remove(link)

        for matnode in mat.node_tree.nodes:
            if matnode.type == "BSDF_PRINCIPLED":
                # desconecto metallic y seteo cero
                if matnode.inputs['Metallic'].is_linked:    
        
                    matnode.inputs["Metallic"].default_value = 0     
                else:
                    matnode.inputs["Metallic"].default_value = 0  
                    matnode.inputs['Specular'].default_value = 0
                   


 
def bake(map):       
    global metalstate               
    #crea imagen
    imgpath = "%s/IMAGES" % (os.path.dirname(bpy.data.filepath))
    img = bpy.data.images.new(channels[map][0],  width=size, height=size, alpha=True)
    print ("Render: %s" % (channels[map][1]))
    if channels[map][0] != "AT":
        img.colorspace_settings.name = 'Linear' 
    img.filepath = "%s/%s_%s.png" % (imgpath, object.name, channels[map][0])
    # creo nodos y bakeo
    for activeMat in mscopy:
        #desmetalizo si no es metalico
        if channels[map][0] != "ME":
            if metalstate == 0:
                metalstate = 1
                desmetalizar(activeMat)        
        
        print(activeMat)
        node = activeMat.node_tree.nodes.new("ShaderNodeTexImage")
        node.image = img
        activeMat.node_tree.nodes.active = node
        node.select = True
    
    bpy.ops.object.bake(type=channels[map][1])
    img.save()
    #bpy.data.images.remove(img)
    #ctiveMat.node_tree.nodes.remove(node)    

    
    

for map in channels.keys():
    bake(map)    
    
    
for matSlot,rms in zip(object.material_slots,ms):
    matSlot.material = rms
        