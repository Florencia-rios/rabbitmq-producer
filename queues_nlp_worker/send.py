import os
import pika
import sys


def send_to_jobs_service_from_nlp():
    credentials = pika.PlainCredentials('flor-rabbit', 'flor1234')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='jobs_with_task_finished', durable=True, arguments={
        "x-queue-type": "quorum"
    })

    channel.exchange_declare(exchange='jobs_with_task_finished_exchange', exchange_type='direct')

    # la routing key se establece como una cadena vacía ''. Esto significa que cualquier mensaje enviado al intercambio
    # main_exchange será enrutado directamente a la cola main_queue
    channel.queue_bind(exchange='jobs_with_task_finished_exchange', queue='jobs', routing_key='')

    # Publica un nuevo mensaje
    channel.basic_publish(exchange='jobs_with_task_finished_exchange',
                          routing_key='',  # La routing key puede ser '' si estás publicando directamente a la cola
                          body='Hello World!')
    print(" [x] Sent 'Hello World!' to jobs_service")

    connection.close()

    return " [x] Sent 'Hello World!'"


if __name__ == '__main__':
    try:
        send_to_jobs_service_from_nlp()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(1)
