import pika
import subprocess
import pymongo

channel = None
credentals = pika.PlainCredentials('rabbitmq', 'rabbitmq')
parameters = pika.ConnectionParameters('rabbit1', 5672, '/', credentals)

mongoClient = pymongo.MongoClient('mongodb://mongo:27017')
myDb = mongoClient['cae']
myCol = myDb['models']

def handle_delivery(channel, method, header, body):
    input_ref = body.decode('utf-8')
    
    myCol.update_one({"fileId": input_ref}, {"$set": {"status": "PRE-STP2GLB"}})

    process_result = subprocess.run(['./step_to_gltf', '-o',
        '/data/cae/stp2glb/' + input_ref, '/data/cae/inputs/' + input_ref])

    if(process_result.returncode == 0):
        print("Success moving to glb2glb")
        myCol.update_one({"fileId": input_ref}, {"$set": {"status": "STP2GLB"}})
        channel.basic_publish(exchange='', routing_key='glb2glb', body=body)
        channel.basic_ack(delivery_tag=method.delivery_tag)
    else:
        print("Failure returning it to the queue")
        myCol.update_one({"fileId": input_ref}, {"$set": {"status": "PREPROCESS"}})
        channel.basic_nack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='stp2glb', durable=True)
channel.queue_declare(queue='glb2glb', durable=True)

channel.basic_consume(queue='stp2glb', auto_ack=False,
        on_message_callback=handle_delivery)

channel.start_consuming()
