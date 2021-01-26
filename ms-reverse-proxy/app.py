#!/usr/bin/python3
import sys
from main.main2 import ProxyServer

if __name__ == '__main__':
    try:
        server = ProxyServer()
        server.run()
    except KeyboardInterrupt as e:
        print ("Ctrl C - Stopping server", e)
        sys.exit(1)
    except Exception as e:
        print ("Stopping server", e)
        sys.exit(1)