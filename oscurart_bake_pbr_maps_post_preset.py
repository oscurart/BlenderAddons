import bpy
import os


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
    meImg.colorspace_settings.name = 'Linear'
    roImg = bpy.data.images.load("%s/%s_RO.png" % (imgpath,token))
    roImg.colorspace_settings.name = 'Linear'

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
        
        
MetallicSmooth(bpy.context.object.active_material.name)         