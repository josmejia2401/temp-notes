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
        if not targetHost:
            abort(403)
            return
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
        return {}, 500


def make_request(url, targetHost, method, headers={}):
    url = '%s/%s' % (targetHost['url'], url)
    logger.info('se recibe la url {}'.format(url))
    host = request.headers.get('host')
    if host:
        headers.update({ "Host" : "%s" % (targetHost['url'])})
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