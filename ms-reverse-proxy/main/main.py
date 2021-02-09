#!/usr/bin/python3
import os
import sys
import threading
import socket
import ssl
from urllib.parse import urlparse
from main.log.log import logger
import copy
import datetime

class RequestDTO:
    def __init__(self, config, conn, client_addr, request, backend_found):
        self.config = copy.deepcopy(config)
        self.conn = conn
        self.client_addr = client_addr
        self.request = request
        self.backend_found = backend_found


class TaskResolve(threading.Thread):
    def __init__(self, request: RequestDTO = None):
        threading.Thread.__init__(self)
        self.request = request
        self.timeOutInSec = float(self.request.config.get_object('server')['timeOutInSec'])
        self.maxDataRecvInByte = int(self.request.config.get_object('server')['maxDataRecvInByte'])

    def run(self):
        s = None
        try:
            self.request.conn.setblocking(False)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(False)
            s.settimeout(self.timeOutInSec)
            url_parse = urlparse(self.request.backend_found['url'])
            s.connect((url_parse.hostname, url_parse.port))
            new_host = bytes('Host: {}:{}'.format(url_parse.hostname, url_parse.port), encoding='utf8')
            current_host = b'Host: localhost:8080'
            request = self.request.request.replace(current_host, new_host)
            s.sendall(request)
            it_response = b''
            while True:
                buffer = s.recv(self.maxDataRecvInByte)
                if buffer and len(buffer) > 0:
                    it_response += buffer
                else:
                    break
            if it_response and len(it_response) > 0:
                self.request.conn.sendall(it_response)
        except socket.error as e:
            logger.error(self.request.backend_found['url'], e)
        except Exception as e:
            logger.error(e)
        finally:
            client_addr = None
            if s: s.close()
            if self.request.conn: self.request.conn.close()

    #def __delete__(self):
    #    pass

#class ProxyServer(threading.Thread):
class ProxyServer(object):

    def __init__(self, config = None):
        #threading.Thread.__init__(self)
        try:
            self.config = config
            self.host = self.config.get_object('server')['host']
            self.port = int(self.config.get_object('server')['port'])
            self.listen = int(self.config.get_object('server')['listen'])
            self.maxDataRecvInByte = int(self.config.get_object('server')['maxDataRecvInByte'])
            self.timeOutInSec = float(self.config.get_object('server')['timeOutInSec'])
            self.running = True
            #definicion del socket
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            self.server.setsockopt(socket.IPPROTO_TCP , socket.TCP_NODELAY, 1)
            self.server.bind((self.host, self.port))
            self.server.listen(self.listen)
            self.server.settimeout(self.timeOutInSec)
            #self.server.setblocking(False)
            logger.info("listening [*] on {}:{}".format(self.host, self.port))
        except socket.error as e:
            logger.error(e)
            if self.server: self.server.close()
            sys.exit(1)
        except Exception as e:
            logger.error(e)
            if self.server: self.server.close()
            sys.exit(1)
    
    def stop(self):
        self.running = False
        if self.server: self.server.close()
        sys.exit(1)

    def run(self):
        logger.info("starting listening")
        while self.running == True:
            conn = None
            try:
                conn, client_addr = self.server.accept()
                request = conn.recv(self.maxDataRecvInByte)
                backend_found = self.__allows_path(request)
                if not backend_found:
                    conn.close()
                else:
                    r = RequestDTO(self.config, conn, client_addr, request, backend_found)
                    taskResolve = TaskResolve(r)
                    taskResolve.daemon = False
                    taskResolve.start()
            except BlockingIOError as e:
                if conn: conn.close()
                continue
            except socket.timeout as e:
                if conn: conn.close()
                continue
            except Exception as e:
                logger.error('Exception', str(e))
                if conn: conn.close()

    def __allows_path(self, request):
        if not request:
            return None
        first_line = str(request).split('\n')[0]
        url = first_line.split(' ')[1]
        targetHost = self.config.get_object('targetHost')
        for target in targetHost:
            if url in target['path']:
                if len(target['methods']) > 0 and self.command in target['methods']:
                    return target
                elif len(target['methods']) == 0:
                    return target
            elif target['path'] in url:
                if len(target['methods']) > 0 and self.command in target['methods']:
                    return target
                elif len(target['methods']) == 0:
                    return target
        return None