import pika
import mysql.connector
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672,heartbeat=120))
channel = connection.channel()
channel.queue_declare(queue='insert_record')

mydb = mysql.connector.connect(
    host="mysql",
    user="user",
    password="password",
    database="student"
)
mycursor = mydb.cursor()

def callback(ch, method, properties, body):
    print("inside callback function-insertion")
    data = body.decode()
    sql = "INSERT INTO student (srn, name, age) VALUES (%s, %s, %s)"
    val = tuple(data.split(','))
    mycursor.execute(sql, val)
    mydb.commit()
    last_id = mycursor.lastrowid
    print("Record inserted with id {}: {}".format(last_id, data))
    print(" [x] %r:%r" % (method.routing_key, body))
    ch.basic_ack(delivery_tag=method.delivery_tag)



channel.basic_qos(prefetch_count=1)
print('before call')
channel.basic_consume(queue='insert_record', on_message_callback=callback)


print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()






