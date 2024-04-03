import os
import sys

from receive_consumer_2 import consume
from send import send

if __name__ == '__main__':
    try:
        consume()
        send()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(1)
        except SystemExit:
            os.exit(1)