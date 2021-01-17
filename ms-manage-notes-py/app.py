from main.main import app, config

if __name__ == '__main__':
    serverConfig = config.get_object('server')
    app.run(host=serverConfig['host'], port=serverConfig['port'], debug=serverConfig['debug'])