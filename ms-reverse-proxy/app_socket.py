from main.main import ProxyServer
from main.util.config import Config

if __name__ == "__main__":
    p = None
    try:
        p = ProxyServer(Config())
        p.run()
    except KeyboardInterrupt as e:
        print(e)
        p.stop()