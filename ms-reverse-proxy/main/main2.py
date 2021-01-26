#!/usr/bin/python3
import os
import sys
import threading
import socket
import ssl
from urllib.parse import urlparse
from main.util.config import Config
from main.log.log import logger
import queue
import time

class MyThread(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.__q = q

    def resolve(self, s):
        try:
            url_parse = urlparse(self.backend_found['url'])
            #ParseResult(scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html', params='', query='', fragment='')
            timeOutInSec = int(self.__configServer['timeOutInSec'])
            maxDataRecvInMB = int(self.__configServer['maxDataRecvInMB'])
            s.settimeout(timeOutInSec)
            logger.info("INICIO - SOCKET establisheding. Peer: de => {} - {} a ==> {} - {}".format(self.client_addr[0], self.client_addr[1], url_parse.hostname, url_parse.port))
            #logger.info("REQUEST: {}".format(self.request))
            s.connect((url_parse.hostname, url_parse.port))
            #logger.info("SOCKET established. Peer: {}".format(s.getpeername()))
            new_host = bytes('Host: {}:{}'.format(url_parse.hostname, url_parse.port), encoding='utf8')
            current_host = b'Host: localhost:8080'
            self.request = self.request.replace(current_host, new_host)
            s.send(self.request)
            while True:
                data = s.recv(maxDataRecvInMB)
                if len(data) > 0:
                    self.conn.send(data)
                else:
                    break
            logger.info("FIN - SOCKET establisheding. Peer: de => {} - {} a ==> {} - {}".format(self.client_addr[0], self.client_addr[1], url_parse.hostname, url_parse.port))
        except socket.error as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)
        finally:
            #if s: s.shutdown(socket.SHUT_RDWR)
            if s: s.close()
            if self.conn: self.conn.close()

    def run(self):
        try:
            while True:
                r = self.__q.get()
                if r is None:
                    time.sleep(0.3)
                    continue
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__configServer = r.config.get_object('server')
                self.conn = r.conn
                self.client_addr = r.client_addr
                self.request = r.request
                self.backend_found = r.backend_found
                self.resolve(s)
        except socket.error as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)
        finally:
            client_addr = None
            self.__q.task_done()

class RequestDTO:
    def __init__(self, config, conn, client_addr, request, backend_found):
        self.config = config
        self.conn = conn
        self.client_addr = client_addr
        self.request = request
        self.backend_found = backend_found


class ProxyServer(object):

    def __init__(self):
        try:
            self.__q = queue.Queue()
            self.__threads = []
            self.__config = Config()
            self.__configServer = self.__config.get_object('server')
            host = self.__configServer['host']
            port = int(self.__configServer['port'])
            listen = int(self.__configServer['listen'])

            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((host, port))
            self.server.listen(listen)
            self.server.setblocking(False)

            logger.info("listening [*] on {}:{}".format(host, port))
        except socket.error as e:
            logger.error(e)
            if self.server: self.server.close()
            sys.exit(1)
        except Exception as e:
            logger.error(e)
            if self.server: self.server.close()
            sys.exit(1)

    def run(self):
        logger.info("starting listening")
        for n in range(0, 5):
            t = MyThread(self.__q)
            t.daemon = False
            t.start()
            self.__threads.append(t)
        while True:
            conn = None
            try:
                try:
                    conn, client_addr = self.server.accept()
                except:
                    time.sleep(0.1)
                    continue
                logger.info('se recibe el host {} {}'.format(client_addr[0], client_addr[1]))
                conn.setblocking(True)
                maxDataRecvInMB = int(self.__configServer['maxDataRecvInMB'])
                request = conn.recv(maxDataRecvInMB)
                backend_found = self.__allows_path(request)
                if not backend_found:
                    conn.close()
                else:
                    r = RequestDTO(self.__config, conn, client_addr, request, backend_found)
                    self.__q.put_nowait(r)
            except Exception as e:
                logger.error(e)
                if conn: conn.close()

    def __allows_path(self, request):
        if not request:
            return None
        first_line = str(request).split('\n')[0]
        url = first_line.split(' ')[1]
        #logger.info('obteniendo url {}'.format(url))
        targetHost = self.__config.get_object('targetHost')
        #logger.info('obteniendo targetHost {}'.format(targetHost))
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