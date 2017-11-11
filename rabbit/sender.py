import pika

connection=pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
channel=connection.channel()
channel.queue_declare(queue='cc')
channel.basic_publish(exchange='',routing_key='cc',body='hello!world!!!')
print("[x] sent 'hello,world!'")
connection.close()

