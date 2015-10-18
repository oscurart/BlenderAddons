# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# AUTHOR: Eugenio Pignataro (Oscurart) www.oscurart.com.ar
# Uso Instrucciones: Crea un collect en zip con todas las imagenes linkeadas al .blend. Abrir la escena y correr. Recordar previamente hacer todos los paths absolutos
# Make a collect with all images linked to blend file. Open the script and run. Remember make all paths absolute first!

import zipfile
import bpy
import os

os.chdir(os.path.dirname(bpy.data.filepath))

with zipfile.ZipFile(r"%s/%s_Collect.zip" % (os.path.dirname(bpy.data.filepath),os.path.basename(bpy.data.filepath).split(".")[0]), mode="w") as file:
    for img in bpy.data.images:
        if img.type not in ["RENDER_RESULT","UV_TEST","COMPOSITING"]:
            file.write(r"%s" % (img.filepath),arcname = os.path.basename(img.filepath))
      