import pika
import time

connection=pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
channel=connection.channel()
channel.queue_declare(queue='task_queue')

def callback(ch,method,properties,body):
        print('[x] Recieved %r'%body)
        time.sleep(body.count(b'.'))
        print("[x] Done")

channel.basic_consume(callback,queue='task_queue',no_ack=True)
# channel.basic_consume(callback,queue='cc')
print('[*] Waiting for msg')
channel.start_consuming()

