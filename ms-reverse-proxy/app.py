#!/usr/bin/python3
import sys, time
from main.main3 import ProxyServer
from main.util.config import Config

if __name__ == '__main__':
    try:
        server = ProxyServer(Config())
        server.start()
        while True:
            time.sleep(5)
    except KeyboardInterrupt as e:
        server.stop()
        print ("Ctrl C - Stopping server", e)
        sys.exit(1)
    except Exception as e:
        server.stop()
        print ("Stopping server", e)
        sys.exit(1)