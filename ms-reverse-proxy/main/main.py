#!/usr/bin/env python3.8


#import BaseHTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
#import urlparse
#import urllib.parse as urlparse
import requests
from main.util.config import Config
import datetime
import json

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def set_header():
    headers = {
        'Host': 'www.google.com'
    }
    return headers

class ProxyHandler (BaseHTTPRequestHandler):
    #__base = BaseHTTPRequestHandler
    #__base_handle = __base.handle
    rbufsize = 0                        # self.rfile Be unbuffered
    allowed_clients = []
    __config = Config()


    def __allows_path(self, path):
        targetHost = self.__config.get_object('targetHost')
        for target in targetHost:
            if path in target['path']:
                return target
            elif target['path'] in path:
                return target
            else:
                return None

    def __response_error(self, code = 500, body = {}):
        self.send_response_only(code)
        x = datetime.datetime.now()
        self.send_header('Date',x.strftime("%c"))
        self.send_header('Content-type','application/json')
        self.send_header('Content-Length',len(json.dumps(body).encode()))
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def do_GET(self, body=True):
        try:
            targetHost = self.__allows_path(self.path)
            if not targetHost:
                body = {"message" : "path not allowed or found"}
                self.__response_error(404, body)
                return
            url = '{}{}'.format(targetHost['url'], self.path)
            req_header = self.parse_headers()
            resp = requests.get(url, headers=merge_two_dicts(req_header, set_header()), verify=False)
            self.send_response(resp.status_code)
            self.send_resp_headers(resp)
            if body:
                self.wfile.write(resp.content)
        except Exception as e:
            self.log_error("Request got ab error out: %r", e)
            body = { "message" : str(e) }
            self.__response_error(500, body)
        finally:
            self.close_connection = 1
    
    def do_POST(self, body=True):
        try:
            targetHost = self.__allows_path(self.path)
            if not targetHost:
                body = {"message" : "path not allowed or found"}
                self.__response_error(404, body)
                return
            url = '{}{}'.format(targetHost['url'], self.path)
            content_len = int(self.headers['content-length'])
            post_body = self.rfile.read(content_len)
            req_header = self.parse_headers()
            resp = requests.post(url, data=post_body, headers=merge_two_dicts(req_header, set_header()), verify=False)
            self.send_response(resp.status_code)
            self.send_resp_headers(resp)
            if body:
                self.wfile.write(resp.content)
                print('resp.content', resp.content)
        except Exception as e:
            self.log_error("Request got ab error out: %r", e)
            body = { "message" : str(e) }
            self.__response_error(500, body)
        finally:
            self.close_connection = 1

    def do_PUT(self, body=True):
        try:
            targetHost = self.__allows_path(self.path)
            if not targetHost:
                body = {"message" : "path not allowed or found"}
                self.__response_error(404, body)
                return
            url = '{}{}'.format(targetHost['url'], self.path)
            content_len = int(self.headers['content-length'])
            post_body = self.rfile.read(content_len)
            req_header = self.parse_headers()
            resp = requests.put(url, data=post_body, headers=merge_two_dicts(req_header, set_header()), verify=False)
            self.send_response(resp.status_code)
            self.send_resp_headers(resp)
            if body:
                self.wfile.write(resp.content)
        except Exception as e:
            self.log_error("Request got ab error out: %r", e)
            body = { "message" : str(e) }
            self.__response_error(500, body)
        finally:
            self.close_connection = 1

    def do_DELETE(self, body=True):
        try:
            targetHost = self.__allows_path(self.path)
            if not targetHost:
                body = {"message" : "path not allowed or found"}
                self.__response_error(404, body)
                return
            url = '{}{}'.format(targetHost['url'], self.path)
            req_header = self.parse_headers()
            resp = requests.delete(url, headers=merge_two_dicts(req_header, set_header()), verify=False)
            self.send_response(resp.status_code)
            self.send_resp_headers(resp)
            if body:
                self.wfile.write(resp.content)
        except Exception as e:
            self.log_error("Request got ab error out: %r", e)
            body = { "message" : str(e) }
            self.__response_error(500, body)
        finally:
            self.close_connection = 1

    def parse_headers(self):
        req_header = {}
        for line in self.headers:
            line_parts = [o.strip() for o in line.split(':', 1)]
            if len(line_parts) == 2:
                req_header[line_parts[0]] = line_parts[1]
        return req_header

    def send_resp_headers(self, resp):
        respheaders = resp.headers
        for key in respheaders:
            if key not in ['Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding', 'content-length', 'Content-Length']:
                self.send_header(key, respheaders[key])
        self.send_header('Content-Length', len(resp.content))
        self.end_headers()

class ThreadingHTTPServer (socketserver.ThreadingMixIn, HTTPServer):
    pass


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
    except Exception as e:
        print(e)
        if httpd:
            httpd.shutdown()
            httpd.server_close()
            httpd.socket.close()