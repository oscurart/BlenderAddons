import bpy
import os

size = 1024

channels = {"albedo":["AT","DIFFUSE"],
    "normal":["NM","NORMAL"],
    "emit":["EM","EMIT"],
    "roughness":["RO","ROUGHNESS"],
    "metallic":["ME","GLOSSY"]}


#set bake options
bpy.context.scene.render.bake_type = "TEXTURE"
bpy.context.scene.render.bake.use_pass_direct = 0
bpy.context.scene.render.bake.use_pass_indirect = 0
bpy.context.scene.render.bake.use_pass_color = 1
bpy.context.scene.render.bake.use_selected_to_active = 0


prps = {}


origMat = bpy.context.object.active_material
activeMat = bpy.context.object.active_material.copy()
bpy.context.object.active_material = activeMat


for node in activeMat.node_tree.nodes:
    if node.type == "BSDF_PRINCIPLED":
        if node.inputs['Metallic'].is_linked:            
            link = activeMat.node_tree.links.new(node.inputs['Specular'],node.inputs['Metallic'].links[0].from_socket)  
            node.inputs["Metallic"].default_value = 0 
            prps[node] = link      
        else:
            prps[node] = node.inputs['Specular'].default_value
            node.inputs['Specular'].default_value = node.inputs['Metallic'].default_value  
            node.inputs["Metallic"].default_value = 0  


for link in activeMat.node_tree.links:
    if link.to_socket.name == "Metallic":
        activeMat.node_tree.links.remove(link)   

for map in channels.keys():
    imgpath = "%s/IMAGES" % (os.path.dirname(bpy.data.filepath))
    img = bpy.data.images.new(channels[map][0],  width=size, height=size, alpha=True)
    print (channels[map][0])
    if channels[map][0] != "AT":
        img.colorspace_settings.name = 'Linear' 
    img.filepath = "%s/%s_%s.png" % (imgpath, activeMat.name.replace(".001",""), channels[map][0])
    node = activeMat.node_tree.nodes.new("ShaderNodeTexImage")
    node.image = img
    activeMat.node_tree.nodes.active = node
    node.select = True
    bpy.ops.object.bake(type=channels[map][1])
    img.save()
    bpy.data.images.remove(img)
    activeMat.node_tree.nodes.remove(node)
    
    
for node,value in prps.items():
    if type(value) == float:
        node.inputs['Specular'].default_value = value    
    else:
        activeMat.node_tree.links.remove(value)
                
bpy.data.materials.remove(activeMat)      
bpy.context.object.active_material = origMat