import bpy
import os
import sys

context = bpy.context
argv = sys.argv

model = argv[argv.index('--') + 1:]
job = argv[argv.index('--') + 2:]
model = model[0]
job = job[0]
model_out_path = "/tmp/"
model_in_path = "/tmp/"

scene = bpy.data.scenes.new("Scene")

inPath = os.path.join(model_in_path, model)
outPath = os.path.join(model_out_path, job)

context.scene.name = model

for scene in bpy.data.scenes:
    for obj in scene.objects:
        obj.select_set(True)
        bpy.ops.object.delete()

bpy.ops.import_scene.gltf(filepath=inPath, filter_glob=".glb")
bpy.ops.export_scene.gltf(export_format="GLB", filepath=outPath)
