import bpy
import os

# cargo el preset de nodos

filepath = "/media/WORKS/3D/PE_PRUEBAS/PERFILES_COLOR/PRESET.blend"
with bpy.data.libraries.load(filepath) as (data_from, data_to):
    data_to.node_groups = data_from.node_groups


# aca reviso si hay nodo de opacidad cargado en el material y seteo salida de 32
opacity = False
bpy.context.scene.render.image_settings.color_depth = "32"

for node in bpy.context.object.data.materials[0].node_tree.nodes:
    if node.type == "TEX_IMAGE":
        if node.image.name.count("_OP"):
            opacity = True

# conecta todo al nodo preset y crea viewer

viewerNode = bpy.context.scene.node_tree.nodes.new("CompositorNodeViewer")
presetNode = bpy.context.scene.node_tree.nodes.new("CompositorNodeGroup")
presetNode.node_tree = bpy.data.node_groups['PRESETS']

for node in bpy.context.object.data.materials[0].node_tree.nodes:
    if node.type == "TEX_IMAGE":
        nodeImage = bpy.context.scene.node_tree.nodes.new("CompositorNodeImage")
        nodeImage.image = node.image
        if node.image.name.count("_AT"):
            bpy.context.scene.node_tree.links.new(bpy.context.scene.node_tree.nodes['Group'].inputs['Albedo'], nodeImage.outputs[0])
        if node.image.name.count("_ME"):
            bpy.context.scene.node_tree.links.new(bpy.context.scene.node_tree.nodes['Group'].inputs['Metallic'], nodeImage.outputs[0])     
        if node.image.name.count("_RO"):
            bpy.context.scene.node_tree.links.new(bpy.context.scene.node_tree.nodes['Group'].inputs['Roughness'], nodeImage.outputs[0]) 
        if node.image.name.count("_OP"):
            bpy.context.scene.node_tree.links.new(bpy.context.scene.node_tree.nodes['Group'].inputs['Opacity'], nodeImage.outputs[0])  

#funcion para renderear
def render(pst):
    bpy.context.scene.node_tree.links.new(viewerNode.inputs[0],
    bpy.context.scene.node_tree.nodes['Group'].outputs[preset])     
    #renderDummy
    bpy.ops.render.render()
    #guardo
    bpy.data.images['Viewer Node'].save_render("%s/IMAGES/Plane_%s_.exr" % (os.path.dirname(bpy.data.filepath),pst)) 


#call para renderear            
for preset in ["MS","AT"]:
    if preset != "AT":
        render(preset)
    else:    
        if opacity == True:
            render(preset)
            
                              