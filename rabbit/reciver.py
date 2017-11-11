import pika

connection=pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
channel=connection.channel()
channel.queue_declare(queue='cc')

def callback(ch,method,properties,body):
        print('[x] Recieved %r'%body)

channel.basic_consume(callback,queue='cc',no_ack=True)
# channel.basic_consume(callback,queue='cc')
print('[*] Waiting for msg')
channel.start_consuming()

