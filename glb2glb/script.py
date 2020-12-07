import bpy
import os
import sys

context = bpy.context
argv = sys.argv

model = argv[argv.index('--') + 1:]
model = model[0]
model_out_path = "/data/cae/glb2glb"
model_in_path = "/data/cae/stp2glb"

scene = bpy.data.scenes.new("Scene")

inPath = os.path.join(model_in_path, model)
outPath = os.path.join(model_out_path, model)

context.scene.name = model

bpy.ops.import_scene.gltf(filepath=inPath, filter_glob=".glb")
bpy.ops.export_scene.gltf(export_format="GLB", filepath=outPath)
