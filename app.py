from flask import Flask, abort, jsonify, request
import thread

from config import SECRET_KEY
import notify
from store import redis


app = Flask(__name__)


@app.errorhandler(401)
def unauthorized(e):
    return jsonify(message=str(e)), 401


@app.before_request
def authenticate():
    if 'CAAS-Auth-Token' not in request.headers:
        abort(401)

    if request.headers['CAAS-Auth-Token'] != SECRET_KEY:
        abort(401)


@app.route('/<label>', methods=['GET'])
def get(label):
    """
    @api {get} /:label Get counter value
    @apiName GetCounter
    @apiGroup Counter

    @apiParam {String} label Counter label.

    @apiSuccess {Number} counter Current value, 0 if label doesn't exist.
    """
    counter = redis.get(label)

    if counter is None:
        counter = 0

    return jsonify(counter=int(counter))


@app.route('/<label>', methods=['PUT'])
def incr(label):
    """
    @api {put} /:label Increment counter
    @apiName IncrementCounter
    @apiGroup Counter

    @apiParam {String} label Counter label.

    @apiSuccess {Number} counter Current value.
    """
    counter = redis.incr(label)
    thread.start_new_thread(notify.gitter, (label, counter))
    return jsonify(counter=counter)


@app.route('/<label>/<int:counter>', methods=['POST'])
def set(label, counter):
    """
    @api {post} /:label/:counter Directly set counter value
    @apiName SetCounter
    @apiGroup Counter

    @apiParam {String} label Counter label.
    @apiParam {Number} counter New counter value.

    @apiSuccess {Number} counter Current value.
    """
    redis.set(label, counter)
    thread.start_new_thread(notify.gitter, (label, counter))
    return jsonify(counter=counter)


@app.route('/<label>', methods=['DELETE'])
def reset(label):
    """
    @api {delete} /:label Reset counter
    @apiName ResetCounter
    @apiGroup Counter

    @apiParam {String} label Counter label.

    @apiSuccess {Number} counter Zero value.
    """
    redis.delete(label)
    return jsonify(counter=0)


if __name__ == '__main__':
    app.run()
