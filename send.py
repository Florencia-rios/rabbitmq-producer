import os
import pika
import sys


def send():

    credentials = pika.PlainCredentials('flor-rabbit', 'flor1234')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='main_queue', durable=True, arguments={
        "x-queue-type": "quorum",
        'x-dead-letter-exchange': 'retry_exchange',
        # Los mensajes rechazados en la cola principal se enviarán a la cola de reintentos, éste es el enrutamiento de los mensajes
        'x-message-ttl': 10000,  # Tiempo de vida del mensaje en la cola principal
        'x-dead-letter-routing-key': 'retry_queue'
    })

    channel.queue_declare(queue='retry_queue', durable=True, arguments={
        "x-queue-type": "quorum",
        'x-dead-letter-exchange': 'main_exchange',
        # Para poder reintentar el procesamiento de los mensajes que hayan sido rechazados por la principal
        'x-message-ttl': 10000,  # Tiempo de vida del mensaje en la cola de reintentos
        'x-dead-letter-routing-key': 'dead_letter_queue',
        # Si se alcanza la cantidad máxima de reintentos los mensajes quedarán en la cola de dead letter
        'x-delivery-limit': 5  # Número máximo de reintentos de los mensajes en ésta cola
    })

    channel.queue_declare(queue='dead_letter_queue', durable=True, arguments={
        "x-queue-type": "quorum"
    })

    # Declaro los exchanges
    channel.exchange_declare(exchange='main_exchange', exchange_type='direct')
    channel.exchange_declare(exchange='retry_exchange', exchange_type='direct')

    # Vinculo las queues y los exchanges
    channel.queue_bind(exchange='main_exchange', queue='main_queue', routing_key='')
    channel.queue_bind(exchange='retry_exchange', queue='retry_queue', routing_key='')

    # Configuro la cola dead_letter_queue para almacenar los mensajes que alcanzaron el número máximo de reintentos
    channel.queue_bind(exchange='retry_exchange', queue='dead_letter_queue', routing_key='')

    # Publica un nuevo mensaje
    channel.basic_publish(exchange='main_exchange',
                          routing_key='',  # La routing key puede ser '' si estás publicando directamente a la cola
                          body='Hello World!')
    print(" [x] Sent 'Hello World!'")

    connection.close()

if __name__ == '__main__':
    try:
        send()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(1)
