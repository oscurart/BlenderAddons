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
else:
    selObject=bpy.context.object    
    
object = bpy.context.object

#lista de materiales originales
if not selected_to_active:
    ms = [mat.material for mat in object.material_slots]
else:
    ms = [mat.material for mat in selObject.material_slots]  
    
    
#sumo materiales copia y reemplazo slots
for matType in ["_glossyTemp","_copyTemp"]:
    ims = 0
    for mat in ms:
        mc = mat.copy()
        mc.name =  mat.name+matType
        if not selected_to_active:
            object.material_slots[ims].material = mc
        else:
            selObject.material_slots[ims].material = mc    
        ims += 1

copyMats = [mat for mat in bpy.data.materials if mat.name.endswith("_copyTemp")]
glossyMats = [mat for mat in bpy.data.materials if mat.name.endswith("_glossyTemp")]


#desmetalizar
def desmetalizar(material):
    for link in mat.node_tree.links:
        if link.to_socket.name == "Metallic":
            mat.node_tree.links.remove(link)
    for matnode in mat.node_tree.nodes:
        if matnode.type == "BSDF_PRINCIPLED":
            # desconecto metallic y seteo cero
            if matnode.inputs['Metallic'].is_linked:           
                matnode.inputs["Metallic"].default_value = 0     
                matnode.inputs["Specular"].default_value = 0    
            else:
                matnode.inputs["Metallic"].default_value = 0  
                matnode.inputs['Specular'].default_value = 0       


#saca todos los speculares
def desespecular(material):
    for matnode in material.node_tree.nodes:
        if matnode.type == "BSDF_PRINCIPLED":
            matnode.inputs["Specular"].default_value = 0 
  
  
#cambia slots
def cambiaSlots(objeto,sufijo):
    for ms in objeto.material_slots:
        ms.material = bpy.data.materials[ms.material.name.rpartition("_")[0]+sufijo] 




#saco los metales en las copias de copy  
for mat in copyMats: 
    desmetalizar(mat)   
    
#saco los metales en las copias de glossy    
for mat in glossyMats: 
    desespecular(mat)                     
 
def bake(map):                    
    #crea imagen
    imgpath = "%s/IMAGES" % (os.path.dirname(bpy.data.filepath))
    img = bpy.data.images.new(channels[map][0],  width=size, height=size, alpha=True)
    print ("Render: %s" % (channels[map][1]))
    if channels[map][0] != "AT":
        img.colorspace_settings.name = 'Linear' 
    if not selected_to_active:        
        img.filepath = "%s/%s_%s.png" % (imgpath, object.name, channels[map][0])
    else:
        img.filepath = "%s/%s_%s.png" % (imgpath, object.active_material.name, channels[map][0])   
        
    #cambio materiales
    if channels[map][0] != "AT":
          cambiaSlots(selObject,"_copyTemp")
    
    if channels[map][0] == "ME":
          cambiaSlots(selObject,"_glossyTemp")                 
          
         
    # creo nodos y bakeo
    if not selected_to_active:
        for activeMat in selObject.data.materials: #aca estaba el mscopy              
            # seteo el nodo
            node = activeMat.node_tree.nodes.new("ShaderNodeTexImage")
            node.image = img
            activeMat.node_tree.nodes.active = node
            node.select = True
    else:
        activeMat = bpy.context.object.active_material               
        # seteo el nodo
        node = activeMat.node_tree.nodes.new("ShaderNodeTexImage")
        node.image = img
        activeMat.node_tree.nodes.active = node
        node.select = True 
  

    bpy.ops.object.bake(type=channels[map][1])
    img.save()
    bpy.data.images.remove(img)
    print ("%s Done!" % (channels[map][1]))
    



#bakeo
for map in channels.keys():
    bake(map)  
    
          
   
#restauro material slots    
for matSlot,rms in zip(selObject.material_slots,ms):
    matSlot.material = rms

#remuevo materiales copia
for ma in copyMats+glossyMats:
    bpy.data.materials.remove(ma)        
  