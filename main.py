import os
import sys

from send_example import send_example

if __name__ == '__main__':
    try:
        send_example()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(1)
        except SystemExit:
            os.exit(1)