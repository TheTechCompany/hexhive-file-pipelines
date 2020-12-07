import pika
import subprocess
import os
import bpy

channel = None
credentals = pika.PlainCredentials('rabbitmq', 'rabbitmq')
parameters = pika.ConnectionParameters('rabbit1', 5672, '/', credentals)

context = bpy.context

model_out_path = "/data/cae/glb2glb"
model_in_path = "/data/cae/stp2glb"

def process(model):
    for scene in bpy.data.scenes:
        for obj in scene.objects:
            scene.objects.unlink(obj)
    scene = bpy.data.scenes.new("Scene")

    inPath = os.path.join(model_in_path, model)
    outPath = os.path.join(model_out_path, model)

    context.scene.name = model

    bpy.ops.import_scene.gltf(filepath=inPath, filter_glob=".glb")
    bpy.ops.export_scene.gltf(export_format="GLB", filepath=outPath)
    return 0;

def handle_delivery(channel, method, header, body):
    print(body)
    input_ref = body.decode('utf-8')
    
    v = process(input_ref)

#    process_result = subprocess.run(args=['blender',
#        '--background', '--python', 'script.py'], env={"Model": input_ref})

    if(v == 0):
        print("Success moving to glb2glb")
        channel.basic_publish(exchange='', routing_key='gltfpack', body=body)
        channel.basic_ack(delivery_tag=method.delivery_tag)
    else:
        print("Failure returning it to the queue")
        channel.basic_nack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='glb2glb', durable=True)
channel.queue_declare(queue='gltfpack', durable=True)

channel.basic_consume(queue='glb2glb', auto_ack=False,
        on_message_callback=handle_delivery)

channel.start_consuming()
