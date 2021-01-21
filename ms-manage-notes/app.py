from main.main import app, config, logger

if __name__ == '__main__':
    try:
        serverConfig = config.get_object('server')
        app.run(host=serverConfig['host'], port=serverConfig['port'], debug=serverConfig['debug'])
    except Exception as e:
        logger.error('app', e)