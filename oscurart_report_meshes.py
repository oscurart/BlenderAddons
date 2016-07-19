import bpy
import os

#this tool write a txt with the selected objects details. 
#save scece, select objects and run


with open("%s" % (bpy.data.filepath.replace(".blend",".txt")), mode="w") as file:
    for ob in bpy.context.selected_objects:
        if ob.type == "MESH":
            file.write("%s\n" % (ob.name))
            #vertices
            file.write("location: %s \n" % (str(ob.location[:])))
            file.write("rotation: %s \n" % (str(ob.rotation_euler[:])))
            file.write("scale: %s \n" % (str(ob.scale[:])))
            file.write("vertices: %s \n" % (str(len(ob.data.vertices))))
            file.write("edges: %s \n" % (str(len(ob.data.edges))))
            file.write("faces: %s \n" % (str(len(ob.data.polygons))))
            tris = 0
            quads = 0
            fgons = 0
            for poly in ob.data.polygons:
                if len(poly.vertices) == 3:
                    tris += 1
                if len(poly.vertices) == 4:
                    quads += 1
                if len(poly.vertices) > 4:
                    fgons += 1                                        
                    
            file.write("tris: %s \n" % (tris))    
            file.write("quads: %s \n" % (quads)) 
            file.write("fgons: %s \n" % (fgons))   
            try:
                file.write("shapes: %s \n" % (len(ob.data.shape_keys.key_blocks)-1))
            except:
                file.write("shapes: %s \n" % ("0"))    
            file.write("\n")
             
            
    
    
    