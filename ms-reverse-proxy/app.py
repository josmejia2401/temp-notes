from urllib.parse import urlparse
from flask import Flask, render_template, request, abort, Response, redirect
import requests
from main.util.config import Config
from main.log.log import logger, logging

app = Flask(__name__)
config = Config()
logging.getLogger('requests').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)
logging.getLogger('requests.packages.urllib3').setLevel(logging.ERROR)


@app.route('/<path:url>', methods=["GET", "POST", "PUT", "DELETE"])
def proxy(url):
    try:
        targetHost = __allows_path(url, request.method)
        logger.info('targetHost {} - {}'.format(url, targetHost))
        if not targetHost:
            #abort(403)
            return {}, 403
        logger.info('se construye la peticion {}'.format(url))
        r = make_request(url, targetHost, request.method, dict(request.headers))
        logger.info('se construye header {}'.format(url))
        headers = dict(r.raw.headers)
        logger.info('se construye header 2 - {}'.format(headers))
        def generate():
            for chunk in r.raw.stream(decode_content=False):
                yield chunk
        logger.info('se construye la salida - {}'.format(headers))
        out = Response(generate(), headers=headers)
        out.status_code = r.status_code
        logger.info('se construye la out - {}'.format(out))
        return out
    except Exception as e:
        logger.error(e)
        return {}, 500


def make_request(url, targetHost, method, headers={}):
    url = '%s/%s' % (targetHost['url'], url)
    logger.info('se recibe la url {}'.format(url))
    host = request.headers.get('host')
    if host:
        headers.update({ "Host" : "%s" % (targetHost['url'])})
    logger.info('make_request - {}'.format(headers))
    if method.upper() == 'GET':
        return requests.request(method, url, params=request.args, stream=True, headers=headers, allow_redirects=False)
    if request.json:
        return requests.request(method, url, params=request.args, stream=True, headers=headers, allow_redirects=False, json=request.json)
    elif request.form:
        return requests.request(method, url, params=request.args, stream=True, headers=headers, allow_redirects=False, data=request.form)
    elif request.data:
        return requests.request(method, url, params=request.args, stream=True, headers=headers, allow_redirects=False, data=request.data)
    else:
        return requests.request(method, url, params=request.args, stream=True, headers=headers, allow_redirects=False)

@app.after_request
def after_request(response):
    response.headers.add(['Access-Control-Allow-Origin'], '*')
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def __allows_path(url, command):
    logger.info('__allows_path {} command {}'.format(url, command))
    if not url:
        return None
    targetHost = config.get_object('targetHost')
    new_url = urlparse('{}/{}'.format('localhost', url))
    for target in targetHost:
        target_url = urlparse('{}/{}'.format('localhost', target['path']))
        if new_url.path in target_url.path:
            return target
        elif target_url.path in new_url.path:
            return target
    return None

if __name__ == "__main__":
    serverConfig = config.get_object('server')
    app.run(host=serverConfig['host'], port=serverConfig['port'], debug=serverConfig['debug'])