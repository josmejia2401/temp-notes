from main.util.config import Config
from flask import Flask, render_template, send_from_directory
import os
#
app = Flask(__name__, static_folder="build", template_folder="build")

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path.startswith('notes/'):
        path = path.replace("notes/", "")
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    serverConfig = Config().get_object('server')
    app.run(host=serverConfig['host'], port=serverConfig['port'], debug=serverConfig['debug'])