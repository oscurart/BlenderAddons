import bpy
import os

bpy.context.scene.render.image_settings.file_format = "PNG"
bpy.context.scene.render.image_settings.color_mode = "RGBA"
bpy.context.scene.render.image_settings.color_depth = "8"
bpy.context.scene.view_settings.view_transform = "sRGB EOTF"
bpy.context.scene.view_settings.gamma = 1

def channelExport(matName,colorMap,alphaMap,outputSufix):
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


    colorImage = bpy.data.images.load("%s/%s%s.png" % (imgpath,matName,colorMap))
    colorImage.colorspace_settings.name = 'sRGB EOTF'
    alphaImage = bpy.data.images.load("%s/%s%s.png" % (imgpath,matName,alphaMap))
    alphaImage.colorspace_settings.name = 'Non-Colour Data'

    meNode = scene.node_tree.nodes.new("CompositorNodeImage")
    meNode.image = colorImage
    
    alphaOver = scene.node_tree.nodes.new("CompositorNodeAlphaOver")
    alphaOver.inputs[1].default_value = (0,0,0,0)

    roNode = scene.node_tree.nodes.new("CompositorNodeImage")
    roNode.image = alphaImage

    viewNode = scene.node_tree.nodes.new("CompositorNodeViewer")


    scene.node_tree.links.new(viewNode.inputs['Image'], alphaOver.outputs['Image'])
    scene.node_tree.links.new(alphaOver.inputs[2], meNode.outputs['Image'])
    scene.node_tree.links.new(alphaOver.inputs[0], roNode.outputs['Image'])

    viewNode.select = 1
    bpy.context.scene.node_tree.nodes.active  = viewNode

    #renderDummy
    bpy.ops.render.render()

    #guardo
    bpy.data.images['Viewer Node'].save_render("%s/%s%s.png" % (imgpath,matName,outputSufix))

    #restauro
    scene.use_nodes = compState
    area3D.type = "VIEW_3D"
    bpy.context.scene.render.resolution_percentage = rp
    scene.node_tree.nodes.remove(meNode)
    scene.node_tree.nodes.remove(roNode)
    scene.node_tree.nodes.remove(viewNode)
    scene.node_tree.nodes.remove(alphaOver)  



#render
channelExport(bpy.context.object.active_material.name,"_ME","_RO","_MS")   
channelExport(bpy.context.object.active_material.name,"_AT","_OP","_ATU")    
   


