import pika
import subprocess
import os

channel = None
credentals = pika.PlainCredentials('rabbitmq', 'rabbitmq')
parameters = pika.ConnectionParameters('rabbit1', 5672, '/', credentals)

def handle_delivery(channel, method, header, body):
    print(body)
    input_ref = body.decode('utf-8')

    process_result = subprocess.run(args=['/usr/local/bin/gltfpack', '-i',
    '/data/cae/glb2glb/' + input_ref + '.glb', '-tc', '-c', '-o',
    '/data/cae/gltfpack/'+ input_ref + '.glb'], env={"Model": input_ref})

    if(process_result.returncode == 0):
        print("Success moving to gltfpack not full success but enough to get us moving")
        channel.basic_ack(delivery_tag=method.delivery_tag)
    else:
        print("Failure returning it to the queue")
        channel.basic_nack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='gltfpack', durable=True)

channel.basic_consume(queue='gltfpack', auto_ack=False,
        on_message_callback=handle_delivery)

channel.start_consuming()
