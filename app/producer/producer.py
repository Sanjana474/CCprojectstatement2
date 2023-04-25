'''import pika
from flask import Flask, request

app = Flask(__name__)
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.exchange_declare(exchange='my_exchange', exchange_type='direct')
queues = ['queue1', 'queue2', 'queue3', 'queue4']
for queue in queues:
    channel.queue_declare(queue=queue)
    channel.queue_bind(exchange='my_exchange', queue=queue, routing_key=queue)

@app.route('/produce', methods=['POST'])
def produce():
    message = request.json
    routing_key = message['routing_key']
    channel.basic_publish(exchange='my_exchange', routing_key=routing_key, body=message['data'])
    return 'Message sent to RabbitMQ'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)'''


import pika
from flask import Flask, request

app = Flask(__name__)
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq',port=5672,heartbeat=120))
channel = connection.channel()
channel.exchange_declare(exchange='my_exchange', exchange_type='direct')
queues = ['health_check', 'insert_record', 'delete_record', 'read_database']
for queue in queues:
    channel.queue_declare(queue=queue)
    channel.queue_bind(exchange='my_exchange', queue=queue, routing_key=queue)

@app.route('/health_check', methods=['GET'])
def health_check():
    message = 'RabbitMQ connection is established'
    routing_key = 'health_check'
    channel.basic_publish(exchange='my_exchange', routing_key=routing_key, body=message)
    return 'Message sent to RabbitMQ'

@app.route('/insert_record', methods=['POST'])
def insert_record():
    data = request.json
    srn = data['SRN']
    name = data['Name']
    age = data['Age']
    message = f'{srn},{name},{age}'
    routing_key = 'insert_record'
    channel.basic_publish(exchange='my_exchange', routing_key=routing_key, body=message)
    return 'Message sent to RabbitMQ'

@app.route('/read_database', methods=['GET'])
def read_database():
    message = 'Get all records from database'
    routing_key = 'read_database'
    channel.basic_publish(exchange='my_exchange', routing_key=routing_key, body=message)
    return 'Message sent to RabbitMQ'

'''@app.route('/read', methods=['GET'])
def read():
    routing_key = 'read_database'
    channel.basic_publish(exchange='my_exchange', routing_key=routing_key, body='')
    return 'Read request sent to RabbitMQ'''

@app.route('/delete', methods=['DELETE'])
def delete():
    srn = request.args.get('srn')
    routing_key = 'delete_record'
    channel.basic_publish(exchange='my_exchange', routing_key=routing_key, body=srn)
    return 'Delete request sent to RabbitMQ'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
