import bpy
import os
# setear un espacio de nodos antes de correr el script

absPath = bpy.path.abspath("//")
imagePath = os.path.join(absPath,"IMAGES")
scene = bpy.context.scene
os.listdir(imagePath)

bpy.context.scene.render.image_settings.file_format = "PNG"
bpy.context.scene.render.image_settings.color_mode = "RGBA"
bpy.context.scene.render.image_settings.color_depth = "8"
bpy.context.scene.view_settings.view_transform = "sRGB EOTF"
bpy.context.scene.view_settings.gamma = 1

scene.use_nodes = True
bpy.context.scene.render.resolution_percentage = 1

viewNode = scene.node_tree.nodes.new("CompositorNodeViewer")
imgNode = scene.node_tree.nodes.new("CompositorNodeImage")
scene.node_tree.links.new(viewNode.inputs[0], imgNode.outputs[0])
viewNode.select = 1
bpy.context.scene.node_tree.nodes.active  = viewNode

for image in os.listdir(imagePath):
    if image.endswith(".exr"):
        print("Procesando: %s" % (image))
        colorImage = bpy.data.images.load(os.path.join(absPath,"IMAGES",image))
        colorImage.use_alpha = 0
        if image.endswith("_AT.exr"):
            colorImage.colorspace_settings.name = 'Non-Colour Data' 
        else:          
            colorImage.colorspace_settings.name = 'sRGB EOTF'
        imgNode.image = colorImage
        bpy.ops.render.render()   
        print(os.path.join(absPath,"IMAGES",image.replace(".exr",".png")))     
        bpy.data.images['Viewer Node'].save_render(os.path.join(absPath,"IMAGES","SKETCHFAB",image.replace(".exr",".png")))
        
 
scene.node_tree.nodes.remove(imgNode)  
scene.node_tree.nodes.remove(viewNode)      
print("---------------------------------------------")    