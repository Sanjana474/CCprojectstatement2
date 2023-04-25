import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672,heartbeat=120))
channel = connection.channel()
channel.queue_declare(queue='health_check')

def callback(ch, method, properties, body):
    
    # Process the message here
    print(f"Received message: {body.decode('utf-8')}")
    print("Received message:{}".format(body))
    # Acknowledge the message
    channel.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='health_check', on_message_callback=callback)

print('Waiting for messages...')
channel.start_consuming()
