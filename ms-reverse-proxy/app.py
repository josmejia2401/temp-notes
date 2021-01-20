from main.main import ProxyHandler, ThreadingHTTPServer
from main.util.config import Config

if __name__ == '__main__':
    httpd = None
    try:
        __config = Config()
        __configServer = __config.get_object('server')
        host = __configServer['host']
        port = int(__configServer['port'])
        httpd = ThreadingHTTPServer((host, port), ProxyHandler)
        httpd.serve_forever()
        httpd.shutdown()
    except KeyboardInterrupt:
        if httpd:
            httpd.shutdown()
            httpd.server_close()
            httpd.socket.close()
    except Exception as e:
        print(e)
        if httpd:
            httpd.shutdown()
            httpd.server_close()
            httpd.socket.close()