from urllib.parse import urlparse,  urljoin
from flask import Flask, render_template, request, Response, redirect
import requests
from main.util.config import Config
from main.log.log import logger, logging

app = Flask(__name__)
config = Config()
logging.getLogger('requests').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)
logging.getLogger('requests.packages.urllib3').setLevel(logging.ERROR)

@app.after_request
def after_request(response):
    response.headers.add(['Access-Control-Allow-Origin'], '*')
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

@app.route('/<path:url>', methods=["GET", "POST", "PUT", "DELETE"])
def proxy(url):
    try:
        targetHost = __allows_path(url, request.method)
        print('url - targetHost', url, targetHost)
        if not targetHost:
            return {}, 403
        r = make_request(url, targetHost, request.method, dict(request.headers))
        headers = dict(r.raw.headers)
        def generate():
            for chunk in r.raw.stream(decode_content=False):
                yield chunk
        out = Response(generate(), headers=headers)
        out.status_code = r.status_code
        return out
    except Exception as e:
        logger.error(e)
        return 'Error interno', 500



def make_request(url, targetHost, method, headers={}):
    if targetHost['ignorePath'] == True:
        targetPath = __normalize_url('', targetHost['path'])
        url = __normalize_url('', url)
        url = url.replace(targetPath, '')
        url = __normalize_url(targetHost['url'], url)
    else:
        url = __normalize_url(targetHost['url'], url)
        
    logger.info('se ha definido false=>', url)
    host = request.headers.get('host')
    if host:
        headers.update({ "Host" : "%s" % (targetHost['url'])})
    
    if method.upper() == 'GET' or method.upper() == 'DELETE':
        return requests.request(method, url, params=request.args, stream=True, headers=headers, allow_redirects=False)
    if request.is_json and request.json and len(request.json) > 0: 
        return requests.request(method, url, params=request.args, stream=True, headers=headers, allow_redirects=False, json=request.json)
    elif request.form and len(request.form) > 0:
        return requests.request(method, url, params=request.args, stream=True, headers=headers, allow_redirects=False, data=request.form)
    elif request.data and len(request.data) > 0:
        return requests.request(method, url, params=request.args, stream=True, headers=headers, allow_redirects=False, data=request.data)
    else:
        return requests.request(method, url, params=request.args, stream=True, headers=headers, allow_redirects=False)


def __normalize_url(url, path):
    if not url.endswith('/'):
        url = url + '/'
    if path.endswith('/'):
        path = path[:-1]
    if path.startswith('/'):
        path = path[1:]
    return urljoin(url, path)

def __allows_path(url, command):
    if not url:
        return None
    targetHost = config.get_object('targetHost')
    new_url = __normalize_url('localhost', url)
    for target in targetHost:
        target_url = __normalize_url('localhost', target['path'])
        if new_url in target_url:
            return target
        elif target_url in new_url:
            return target
    return None

if __name__ == "__main__":
    serverConfig = config.get_object('server')
    app.run(host=serverConfig['host'], port=serverConfig['port'], debug=serverConfig['debug'])