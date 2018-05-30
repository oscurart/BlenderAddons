import bpy
import os

# VARIABLES
size = 128
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
object = bpy.context.object


if selected_to_active:
    #hago el merge
    bpy.ops.object.select_all(action="DESELECT")
    for o in selectedObjects:
        o.select = True
    bpy.context.scene.objects.active  = selectedObjects[0]
    bpy.ops.object.convert(target="MESH", keep_original=True)
    selObject = bpy.context.active_object
    bpy.ops.object.join()
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True, properties=True)
else:
    selObject=bpy.context.object    

bpy.context.scene.objects.active  = object 

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




# mezcloGlossy
def mixGlossy(material):
    mat = material

    for node in mat.node_tree.nodes[:]:
        if node.type == "BSDF_PRINCIPLED":            
            nprin = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled") # nuevo principled

            mix = mat.node_tree.nodes.new("ShaderNodeMixShader")
            mat.node_tree.links.new(mix.inputs[2],nprin.outputs[0])
            mat.node_tree.links.new(mix.inputs[1],node.outputs[0]) 
            if node.inputs["Metallic"].is_linked:  
                mat.node_tree.links.new(mix.inputs[0],node.inputs['Metallic'].links[0].from_socket)    
            else:
                mix.inputs[0].default_value = node.inputs['Metallic'].default_value
            
            #copio metalico
            if node.inputs["Metallic"].is_linked:        
                mat.node_tree.links.new(mix.inputs[0],node.inputs["Metallic"].links[0].from_socket)
            mat.node_tree.links.new(node.outputs['BSDF'].links[0].to_socket,mix.outputs[0])
            
            #copio seteos de p a p
            for entrada in ["Base Color","Roughness"]:
                if node.inputs[entrada].is_linked:
                      mat.node_tree.links.new(nprin.inputs[entrada],node.inputs[entrada].links[0].from_socket)
                nprin.inputs[entrada].default_value =  node.inputs[entrada].default_value        
                                      
            node.inputs['Specular'].default_value = 0 
            node.inputs['Metallic'].default_value = 0 # ambos a cero
            nprin.inputs['Specular'].default_value = 0 
            nprin.inputs['Metallic'].default_value = 1 # nuevo prin a 1

    for link in mat.node_tree.links:
        if link.to_socket.name == "Metallic":
            mat.node_tree.links.remove(link)   


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
    mixGlossy(mat) 
    
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
        activeMat = object.active_material               
        # seteo el nodo
        node = activeMat.node_tree.nodes.new("ShaderNodeTexImage")
        node.image = img
        activeMat.node_tree.nodes.active = node
        node.select = True 
  

    bpy.ops.object.bake(type=channels[map][1])
    img.save()
    bpy.data.images.remove(img)
    print ("%s Done!" % (channels[map][1]))
    

def MetallicSmooth(token):
    scene = bpy.context.scene
    #guardo el porcentaje
    rp = bpy.context.scene.render.resolution_percentage
    bpy.context.scene.render.resolution_percentage = 1
    #habilito el editor de nodos
    compState = scene.use_nodes
    scene.use_nodes = True

    #seteo las areas 3d a editor de nodos
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            area.type = "NODE_EDITOR"
            area.spaces[0].show_backdrop = 1
            area3D = area
            
    #seteo el path de las imagenes        
    imgpath = "%s/IMAGES" % (os.path.dirname(bpy.data.filepath))


    meImg = bpy.data.images.load("%s/%s_ME.png" % (imgpath,token)) #CAMBIAAAAAAAAAR
    roImg = bpy.data.images.load("%s/%s_RO.png" % (imgpath,token))

    meNode = scene.node_tree.nodes.new("CompositorNodeImage")
    meNode.image = meImg

    roNode = scene.node_tree.nodes.new("CompositorNodeImage")
    roNode.image = roImg

    invert = scene.node_tree.nodes.new("CompositorNodeInvert")

    viewNode = scene.node_tree.nodes.new("CompositorNodeViewer")


    scene.node_tree.links.new(viewNode.inputs['Image'], meNode.outputs['Image'])
    scene.node_tree.links.new(viewNode.inputs['Alpha'], invert.outputs['Color'])
    scene.node_tree.links.new(invert.inputs['Color'], roNode.outputs['Image'])

    viewNode.select = 1
    bpy.context.scene.node_tree.nodes.active  = viewNode

    #renderDummy
    bpy.ops.render.render()

    #guardo
    bpy.data.images['Viewer Node'].save_render("%s/%s_MS.png" % (imgpath,token))

    #restauro
    scene.use_nodes = compState
    area3D.type = "VIEW_3D"
    bpy.context.scene.render.resolution_percentage = rp
    scene.node_tree.nodes.remove(meNode)
    scene.node_tree.nodes.remove(roNode)
    scene.node_tree.nodes.remove(viewNode)
    scene.node_tree.nodes.remove(invert)    
        
    

#bakeo
for map in channels.keys():
    bake(map)  

#Rendereo el MS   

if not selected_to_active:  
    MetallicSmooth(object.name)       

else:
    MetallicSmooth(object.active_material.name) 
         
   
#restauro material slots    
for matSlot,rms in zip(selObject.material_slots,ms):
    matSlot.material = rms

#remuevo materiales copia
for ma in copyMats+glossyMats:
    bpy.data.materials.remove(ma)        

  
#borro el merge
if selected_to_active:
    bpy.data.objects.remove(selObject, do_unlink=True, do_id_user=True, do_ui_user=True)