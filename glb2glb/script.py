import bpy
import os

context = bpy.context

model_path = "/glb2glb"
model = "exported.glb"

scene = bpy.data.scenes.new("Scene")

path = os.path.join(model_path, model)

context.scene.name = model

bpy.ops.import_scene.gltf(filepath=path, filter_glob=".glb")

bpy.ops.export_scene.gltf(export_format="GLB", filepath=os.path.join(model_path, "repacked.glb"))
