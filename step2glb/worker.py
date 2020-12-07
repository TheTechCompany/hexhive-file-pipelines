import pika
import subprocess

channel = None
credentals = pika.PlainCredentials('rabbitmq', 'rabbitmq')
parameters = pika.ConnectionParameters('rabbit1', 5672, '/', credentals)

def handle_delivery(channel, method, header, body):
    print(body)
    input_ref = body.decode('utf-8')
    process_result = subprocess.run(args=['./step_to_gltf', '-o', '/data/cae/stp2glb/' + input_ref, '/data/cae/inputs/' + input_ref], capture_output=True)

    if(process_result.returncode == 0):
        channel.basic_ack(delivery_tag=method.delivery_tag)
    else:
        channel.basic_nack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='stp2glb', durable=True)

channel.basic_consume(queue='stp2glb', auto_ack=False,
        on_message_callback=handle_delivery)

channel.start_consuming()
