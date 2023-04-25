import pika
import mysql.connector

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672, heartbeat=120))
channel = connection.channel()

channel.queue_declare(queue='read_database')
mydb = mysql.connector.connect(
    host="mysql",
    user="user",
    password="password",
    database="student"
)
mycursor = mydb.cursor()

def callback(ch, method, properties, body):
    print("inside callback function-read")
    mycursor.execute("SELECT * FROM student")
    rows = mycursor.fetchall()
    for row in rows:
        print(row)
        

channel.basic_consume(queue='read_database', on_message_callback=callback, auto_ack=True)

channel.start_consuming()
