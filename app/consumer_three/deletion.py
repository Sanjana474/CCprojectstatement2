import pika
import mysql.connector

# connect to MySQL database
db = mysql.connector.connect(
  host="mysql",
  user="user",
  password="password",
  database="student"
)

# create a cursor object
cursor = db.cursor()

# connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672,heartbeat=120))
channel = connection.channel()

# create a queue for delete_record
channel.queue_declare(queue='delete_record')

# define callback function for incoming messages
def callback(ch, method, properties, body):
    print("inside callback function-deletion")
    # get the SRN from the message body
    srn = body.decode('utf-8')
    
    # delete the record from the database
    sql = "DELETE FROM student WHERE srn = %s"
    cursor.execute(sql, (srn,))
    db.commit()
    
    # acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)


# start consuming messages from the queue
channel.basic_consume(queue='delete_record', on_message_callback=callback)

# run the consumer
channel.start_consuming()
