import os
import pika
import sys


def consume():
    credentials = pika.PlainCredentials('flor-rabbit', 'flor1234')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()

    # Cola de tipo quorum, por default es durable=true
    channel.queue_declare(queue='prueba_quorum', durable=True, arguments={"x-queue-type": "quorum"})

    # el auto_ack=True es para confirmar que ya llegó el mensaje de manera automática, pero se podría configurar para que
    # avise bajo cierta condición si llego o no el mensaje, si no llega, se enviaría a la cola de reintentos
    channel.basic_consume(queue='prueba_quorum', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    # inicia el bucle de consumo de mensajes y tu la aplicación va a quedar esperando a los mensajes
    channel.start_consuming()


# Esta función se ejecutará cada vez que llegue un mensaje, en este caso, sólo lo imprime
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")


if __name__ == '__main__':
    try:
        consume()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(1)