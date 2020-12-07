import pika
import subprocess
import os
from subprocess import PIPE
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

    myCol.update_one({"fileId": input_ref}, {"$set": {"status": "PRE-GLB2GLB"}})

    process_result = subprocess.run(args=['blender', '--background',
        '--python', 'script.py', '--', input_ref], env={"Model": input_ref},
        stdout=PIPE, stderr=PIPE)

    stdout = process_result.stdout.decode('utf-8')
    try:
        index = stdout.index('Finished glTF 2.0 export')
        print("Success moving to glb2glb not full success but enough to get us moving")
        myCol.update_one({"fileId": input_ref}, {"$set": {"status": "GLB2GLB"}})
        channel.basic_publish(exchange='', routing_key='gltfpack', body=body)
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except ValueError:
        print("Failure returning it to the queue")
        myCol.update_one({"fileId": input_ref}, {"$set": {"status": "STP2GLB"}})
        channel.basic_nack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='glb2glb', durable=True)
channel.queue_declare(queue='gltfpack', durable=True)

channel.basic_consume(queue='glb2glb', auto_ack=False,
        on_message_callback=handle_delivery)

channel.start_consuming()
