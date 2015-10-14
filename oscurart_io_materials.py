import bpy
import json
 
def guarda():
    # nodes
    matlist = {}
    for mat in bpy.data.materials:
        nodes = {node.name : {
            "type" : node.rna_type.identifier,
            "location":tuple(node.location[:]),
            "name":node.name,
            "inputRaw" : {input : i  for i,input in enumerate(node.inputs)},
            "outputRaw" : {input : i  for i,input in enumerate(node.outputs)},
            "input": {i: 
                {"name":input.name,
                "type":input.type,
                "default_value":input.default_value[:] if input.type in ["RGBA","VECTOR"] else input.default_value if input.type == "VALUE" else None
                } 
                for i,input in enumerate(node.inputs)
                },
            "output": {i: 
                {"name":output.name,
                "type":output.type,
                "default_value":output.default_value[:] if output.type in ["RGBA","VECTOR"] else output.default_value if output.type == "VALUE" else None
                } 
                for i,output in enumerate(node.outputs)
                },
            }
            for node in mat.node_tree.nodes}        
        # links 
        links = {i:{
            "input":{"node":link.to_node.name,"socket":nodes[link.to_node.name]['inputRaw'][link.to_socket]},
            "output":{"node":link.from_node.name,"socket":nodes[link.from_node.name]['outputRaw'][link.from_socket]}
            }
            for i,link in enumerate(mat.node_tree.links)}        
        # pop raws
        for node in nodes:
            nodes[node].pop("inputRaw")
            nodes[node].pop("outputRaw")
        matlist[mat.name] = {"nodes":nodes,"links":links}
    # exporta
    filepath = bpy.data.filepath.replace(".blend",".json")
    with open(filepath, "w") as file:
        json.dump(matlist, file, ensure_ascii=False) 
  

def carga ():
    # carga
    filepath = bpy.data.filepath.replace(".blend",".json")
    with open(filepath, "r") as file:    
        rf = json.load(file)    

    for imat in rf:
        # nodos
        mat = bpy.data.materials.new(imat)
        mat.use_nodes = True
        # remove nodes
        for node in mat.node_tree.nodes:
            mat.node_tree.nodes.remove(node)
        for node in rf[imat]["nodes"]:            
            nd = mat.node_tree.nodes.new(rf[imat]["nodes"][node]["type"])            
            nd.location = rf[imat]["nodes"][node]['location']#
            for i,input in enumerate(nd.inputs):
                if input.type != "SHADER" and rf[imat]["nodes"][node]["type"] != "NodeReroute":
                    input.default_value = rf[imat]["nodes"][node]['input'][str(i)]["default_value"]
            for i,output in enumerate(nd.outputs):
                if output.type != "SHADER" and rf[imat]["nodes"][node]["type"] != "NodeReroute":
                    output.default_value = rf[imat]["nodes"][node]['output'][str(i)]["default_value"]  
        for link in rf[imat]["links"]:
            ln = mat.node_tree.links.new(
                mat.node_tree.nodes[rf[imat]["links"][link]['input']['node']].inputs[rf[imat]["links"][link]['input']['socket']],
                mat.node_tree.nodes[rf[imat]["links"][link]['output']['node']].outputs[rf[imat]["links"][link]['output']['socket']]
                ) 


guarda()
#carga()