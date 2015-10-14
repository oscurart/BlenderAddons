import bpy
import os
import json

path = "Z:/rnd_tronco/blender/presets"

def savePresets(ins):
    # scene
    if ins == 1:        
        sceneCompound = {}
        sceneCompound["sceneset"] = {i : getattr(bpy.context.scene, i) for i in dir(bpy.context.scene)  if type(getattr(bpy.context.scene, i)) in [str,float,int,bool]}
        with open(os.path.join(path,"scene.json"),"w") as file:
            json.dump(sceneCompound,file)     
    # render           
    if ins == 2:    
        renderCompound = {}
        renderCompound["renderset"] = {i : getattr(bpy.context.scene.render, i) for i in dir(bpy.context.scene.render)  if type(getattr(bpy.context.scene.render, i)) in [str,float,int,bool]}
        renderCompound["imageformatset"] = {i : getattr(bpy.context.scene.render.image_settings, i) for i in dir(bpy.context.scene.render.image_settings)  if type(getattr(bpy.context.scene.render.image_settings, i)) in [str,float,int,bool]}
        with open(os.path.join(path,"render.json"),"w") as file:
            json.dump(renderCompound,file)     
    # cycles        
    if ins == 3:    
        cyclesCompound = {}
        cyclesCompound["cyclesset"] = {i : getattr(bpy.context.scene.cycles, i) for i in dir(bpy.context.scene.cycles)  if type(getattr(bpy.context.scene.cycles, i)) in [str,float,int,bool]}
        with open(os.path.join(path,"cycles.json"),"w") as file:
            json.dump(cyclesCompound,file)                 

def loadPresets(ins):
    if ins == 1:
        with open(os.path.join(path,"scene.json"),"r") as file:
            sceneset = json.load(file)  
        for i in sceneset["sceneset"]:
            if i not in ["name","frame_start","frame_end"]:
                try:
                    setattr(bpy.context.scene,i,sceneset["sceneset"][i])   
                except:
                    print(i)   
    if ins == 2:
        with open(os.path.join(path,"render.json"),"r") as file:
            renderset = json.load(file)   
        #render                      
        for i in renderset['renderset'] :
            if i not in ["filepath"]:
                try:
                    setattr(bpy.context.scene.render,i,renderset['renderset'][i])
                except:
                    print(i)
        #imagesettings
        for i in renderset['imageformatset'] :
            try:
                setattr(bpy.context.scene.render.image_settings,i,renderset['imageformatset'][i])
            except:
                print(i)  
    if ins == 3:
        with open(os.path.join(path,"cycles.json"),"r") as file:
            cyclesset = json.load(file)  
        for i in cyclesset["cyclesset"]:
            try:
                setattr(bpy.context.scene.cycles,i,cyclesset["cyclesset"][i])   
            except:
                print(i)                   
# 1-scene 2-render 3-cycles           
#savePresets(1)    
#savePresets(2)  
#savePresets(3)  
loadPresets(1)  
loadPresets(2)   
loadPresets(3)    