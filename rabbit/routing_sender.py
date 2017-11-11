import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'queue1'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='direct_logs',
                        routing_key=severity,
                        body=message,properties=pika.BasicProperties(
                        delivery_mode=2,  # 消息持久化
                    ))
print(" [x] Sent %r:%r" % (severity, message))
connection.close()  