import pika

channel = None
credentals = pika.PlainCredentials('rabbitmq', 'rabbitmq')
parameters = pika.ConnectionParameters('rabbit1', 5672, '/', credentals)

def on_connected(connection):
    connection.channel(on_open_callback=on_channel_open)

def on_channel_open(new_channel):
    global channel
    channel = new_channel
    consume()
#    channel.queue_declare(queue="stp2glb", durable=T

def consume():
    channel.basic_consume("stp2glb", handle_delivery)

def handle_delivery(channel, method, header, body):
    print(body)

connection = pika.SelectConnection(parameters, on_open_callback=on_connected)

try:
    connection.ioloop.start()
except KeyboardInterrupt:
    connection.close()
    connection.ioloop.start()
