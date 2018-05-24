import bpy
import os

# VARIABLES
size = 512
selected_to_active= True


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

selectedObjects = bpy.context.selected_objects[:].copy()
selectedObjects.remove(bpy.context.active_object)
if selected_to_active:
    selObject=selectedObjects[0]
    
object = bpy.context.object

metalstate = 0 #variable que indica que ya se desmetalizo.

#lista de materiales originales y copias
if not selected_to_active:
    ms = [mat.material for mat in object.material_slots]
else:
    ms = [mat.material for mat in selObject.material_slots]  
    
mscopy = []
    
#sumo materiales copia y reemplazo slots
ims = 0
for mat in ms:
    mc = mat.copy()
    mscopy.append(mc)
    if not selected_to_active:
        object.material_slots[ims].material = mc
    else:
        selObject.material_slots[ims].material = mc    
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
    if not selected_to_active:
        for activeMat in mscopy:
            #desmetalizo si no es metalico
            if channels[map][0] != "ME":
                if metalstate == 0:
                    metalstate = 1
                    desmetalizar(activeMat)        
            
            # seteo el nodo
            print(activeMat)
            node = activeMat.node_tree.nodes.new("ShaderNodeTexImage")
            node.image = img
            activeMat.node_tree.nodes.active = node
            node.select = True
    else:
        print(object.active_material)
        activeMat = bpy.context.object.active_material        
        #desmetalizo si no es metalico
        if channels[map][0] != "ME":
            if metalstate == 0:
                metalstate = 1
                desmetalizar(activeMat)  
                
        # seteo el nodo
        node = activeMat.node_tree.nodes.new("ShaderNodeTexImage")
        node.image = img
        activeMat.node_tree.nodes.active = node
        node.select = True                
                               
        
    bpy.ops.object.bake(type=channels[map][1])
    img.save()
    bpy.data.images.remove(img)
    



#bakeo
for map in channels.keys():
    bake(map)  
    
          
   
#restauro material slots    
for matSlot,rms in zip(selObject.material_slots,ms):
    matSlot.material = rms

#remuevo materiales copia
for ma in mscopy:
    bpy.data.materials.remove(ma)        
   