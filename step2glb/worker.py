import pika

channel = None
credentals = pika.PlainCredentials('rabbitmq', 'rabbitmq')
parameters = pika.ConnectionParameters('rabbit1', 5672, '/', credentals)

def on_connected(connection):
    print("Connected to rabbitmq")
    connection.channel(on_open_callback=on_channel_open)

def on_channel_open(new_channel):
    print("Channel opened")
    global channel
    channel = new_channel
    consume()
#    channel.queue_declare(queue="stp2glb", durable=T

def consume():
    print("Consuming")
    channel.basic_consume("stp2glb", handle_delivery)

def handle_delivery(channel, method, header, body):
    print("STUFF")
    print(body)

connection = pika.SelectConnection(parameters, on_open_callback=on_connected)

try:
    connection.ioloop.start()
except KeyboardInterrupt:
    connection.close()
    connection.ioloop.start()
