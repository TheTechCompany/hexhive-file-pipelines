import pika
import subprocess

channel = None
credentals = pika.PlainCredentials('rabbitmq', 'rabbitmq')
parameters = pika.ConnectionParameters('rabbit1', 5672, '/', credentals)

def handle_delivery(channel, method, header, body):
    print(body)
    input_ref = body.decode('utf-8')
    process_result = subprocess.run(['MODEL=' + input_ref, 'blender',
        '--background', '--python', 'script.py'])

    if(process_result.returncode == 0):
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
