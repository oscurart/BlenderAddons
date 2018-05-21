import bpy
import os

size = 2048

channels = {"albedo":["AT","DIFFUSE"],
    "normal":["NM","NORMAL"],
    "emit":["EM","EMIT"],
    "roughness":["RO","ROUGHNESS"],
    "glossy":["GL","GLOSSY"]}


#set bake options
bpy.context.scene.render.bake_type = "TEXTURE"
bpy.context.scene.render.bake.use_pass_direct = 0
bpy.context.scene.render.bake.use_pass_indirect = 0
bpy.context.scene.render.bake.use_pass_color = 1
bpy.context.scene.render.bake.use_selected_to_active = 0

for map in channels.keys():
    imgpath = "%s/IMAGES" % (os.path.dirname(bpy.data.filepath))
    activeMat = bpy.context.object.active_material
    img = bpy.data.images.new(channels[map][0],  width=size, height=size, alpha=True)
    print (channels[map][0])
    if channels[map][0] != "AT":
        img.colorspace_settings.name = 'Linear' 
    img.filepath = "%s/%s_%s.png" % (imgpath, activeMat.name, channels[map][0])
    node = activeMat.node_tree.nodes.new("ShaderNodeTexImage")
    node.image = img
    activeMat.node_tree.nodes.active = node
    node.select = True
    bpy.ops.object.bake(type=channels[map][1])
    img.save()
    bpy.data.images.remove(img)
    activeMat.node_tree.nodes.remove(node)