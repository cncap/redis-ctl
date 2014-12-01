import functools
import logging
import flask

import file_ipc
import redisctl.errors


def jsonify(result, status_code=200):
    r = flask.jsonify(**result)
    r.status_code = status_code
    return r


def init_app(manager, debug):
    app = flask.Flask('RedisController', static_folder=None)
    app.debug = debug

    @app.route('/', methods=['GET'])
    def index():
        return flask.render_template('index.html', instances=file_ipc.read())

    def handle(uri, method):
        def wrapper(f):
            @app.route(uri, methods=[method])
            @functools.wraps(f)
            def handle_func(*args, **kwargs):
                try:
                    return jsonify(f(*args, **kwargs))
                except redisctl.errors.AppMutexError:
                    return jsonify({'reason': 'app occupying'}, 400)
                except redisctl.errors.AppUninitError:
                    return jsonify({'reason': 'start not called'}, 400)
                except redisctl.errors.InstanceExhausted:
                    return jsonify({'reason': 'instance exhausted'}, 500)
                except redisctl.errors.RemoteServiceFault:
                    logging.exception(e)
                    return jsonify({'reason': 'remote service fault'}, 500)
                except StandardError, e:
                    logging.error('UNEXPECTED ERROR')
                    logging.exception(e)
                    return jsonify({'reason': 'unexpected', 'msg': e.message},
                                   500)
            return handle_func
        return wrapper

    @handle('/start/<appname>', 'POST')
    def request_cluster(appname):
        logging.info('Request start cluster for %s', appname)
        instance = manager.app_start(appname)
        logging.info('Distribute* instance %s:%d to %s', instance['host'],
                     instance['port'], appname)
        return instance

    @handle('/expand/<appname>', 'POST')
    def request_expand(appname):
        logging.info('Request new instance for %s', appname)
        instance = manager.app_expand(appname)
        logging.info('Distribute+ instance %s:%d to %s', instance['host'],
                     instance['port'], appname)
        return instance

    return app