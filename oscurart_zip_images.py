# abrir la escena y correr. Recordar previamente hacer todos los paths absolutos

import zipfile
import bpy
import os

os.chdir(os.path.dirname(bpy.data.filepath))

with zipfile.ZipFile(r"%s/%s_Collect.zip" % (os.path.dirname(bpy.data.filepath),os.path.basename(bpy.data.filepath).split(".")[0]), mode="w") as file:
    for img in bpy.data.images:
        if img.type not in ["RENDER_RESULT","UV_TEST","COMPOSITING"]:
            file.write(r"%s" % (img.filepath),arcname = os.path.basename(img.filepath))
      