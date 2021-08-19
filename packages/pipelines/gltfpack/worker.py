import pika
import subprocess
import os
import pymongo

channel = None
credentals = pika.PlainCredentials('rabbitmq', 'rabbitmq')
parameters = pika.ConnectionParameters('rabbit1', 5672, '/', credentals)

mongoClient = pymongo.MongoClient('mongodb://mongo:27017')
myDb = mongoClient['cae']
myCol = myDb['models']

def handle_delivery(channel, method, header, body):
    print(body)
    input_ref = body.decode('utf-8')

    myCol.update_one({"fileId": input_ref}, {"$set": {"status": "PREPACK"}})

    os.chdir("/data/cae/glb2glb")
    process_result = subprocess.run(args=['/usr/local/bin/gltfpack', '-i',
    './' + input_ref + '.glb', '-tc', '-kn', '-km', '-c', '-o',
    '../gltfpack/'+ input_ref + '.glb'], env={"Model": input_ref})

    if(process_result.returncode == 0):
        myCol.update_one({"fileId": input_ref}, {"$set": {"status": "PACKED"}})
        print("Success moving to gltfpack not full success but enough to get us moving")
        channel.basic_ack(delivery_tag=method.delivery_tag)
    else:
        myCol.update_one({"fileId": input_ref}, {"$set": {"status": "GLB2GLB"}})
        print("Failure returning it to the queue")
        channel.basic_nack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='gltfpack', durable=True)

channel.basic_consume(queue='gltfpack', auto_ack=False,
        on_message_callback=handle_delivery)

channel.start_consuming()
