import pika
import sys
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
print(queue_name)
severities = sys.argv[1:]
if not severities:
    print(sys.stderr, "Usage: %s [info] [warning] [error]" % (sys.argv[0],))
    sys.exit(1)

for severity in severities:
    print(queue_name)
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    time.sleep(5)
    print(" [x] %r:%r" % (method.routing_key, body))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(callback, queue=queue_name)

channel.start_consuming()