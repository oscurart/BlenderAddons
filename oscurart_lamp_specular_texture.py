import bpy

ob = bpy.context.object

if ob.type == "LAMP":
    if ob.data.type == "AREA":
        ob.data.use_nodes = True
        ob.data.cycles.use_multiple_importance_sampling = True
        #nodos nuevos
        pos = bpy.context.object.data.node_tree.nodes.new("ShaderNodeNewGeometry")
        img = bpy.context.object.data.node_tree.nodes.new("ShaderNodeTexImage")
        snm1 = ob.data.node_tree.nodes.new("ShaderNodeMapping")
        snm2 = ob.data.node_tree.nodes.new("ShaderNodeMapping")
        #conexion        
        inImg = img.inputs['Vector']
        outImg = img.outputs['Color']
        snm1.vector_type = "TEXTURE"
        snm2.vector_type = "TEXTURE"
        outPos = pos.outputs['Position']
        inMapping1 = snm1.inputs['Vector']
        outMapping1 = snm1.outputs['Vector']
        inMapping2 = snm2.inputs['Vector']
        outMapping2 = snm2.outputs['Vector']        
        ob.data.node_tree.links.new(inMapping1,outPos)
        ob.data.node_tree.links.new(outMapping1,inMapping2)
        ob.data.node_tree.links.new(inImg,outMapping2)
        ob.data.node_tree.links.new(ob.data.node_tree.nodes['Emission'].inputs['Color'],outImg)
        # drivers
        dr1 = snm1.driver_add("translation")
        dr2 = snm1.driver_add("rotation")
        dr3 = snm2.driver_add("translation")
        dr4 =snm2.driver_add("scale")
        # conecto drivers  
        coordict = {0:"X",1:"Y",2:"Z","rotation":"ROT","translation":"LOC","scale":"SCALE"}
        for driver in [dr1,dr2]:
            for i in driver:
                var = i.driver.variables.new()
                var.targets[0].id = ob
                var.type = "TRANSFORMS"
                i.driver.expression = "var"
                print(coordict[i.data_path.rsplit(".")[-1]])
                var.targets[0].transform_type = "%s_%s" % (coordict[i.data_path.rsplit(".")[-1]],coordict[i.array_index])                
        # scale segundo mapping
        for i in dr3:
            var = i.driver.variables.new()
            var.targets[0].id = ob
            var.type = "SINGLE_PROP"
            i.driver.expression = "var/2"
            print(coordict[i.data_path.rsplit(".")[-1]])
            var.targets[0].transform_type = "%s_%s" % (coordict[i.data_path.rsplit(".")[-1]],coordict[i.array_index])  
            var.targets[0].id_type = "LAMP"   
            var.targets[0].id = ob.data  
            var.targets[0].data_path = "size"
        # scale tercer mapping    
        for i in dr4:
            var = i.driver.variables.new()
            var.targets[0].id = ob
            var.type = "SINGLE_PROP"
            i.driver.expression = "var"
            print(coordict[i.data_path.rsplit(".")[-1]])
            var.targets[0].transform_type = "%s_%s" % (coordict[i.data_path.rsplit(".")[-1]],coordict[i.array_index])  
            var.targets[0].id_type = "LAMP"   
            var.targets[0].id = ob.data  
            var.targets[0].data_path = "size"      
else:
    print("NO LAMP OBJECT SELECTED!")                  