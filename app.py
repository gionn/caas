from flask import Flask, abort, jsonify, request

from config import SECRET_KEY
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
    counter = redis.get(label)

    if counter is None:
        counter = redis.incr(label)

    return jsonify(counter=int(counter))


@app.route('/<label>', methods=['PUT'])
def incr(label):
    counter = redis.incr(label)
    return jsonify(counter=counter)


@app.route('/<label>/<int:counter>', methods=['POST'])
def set(label, counter):
    redis.set(label, counter)
    return jsonify(counter=counter)


@app.route('/<label>', methods=['DELETE'])
def reset(label):
    counter = redis.delete(label)
    return jsonify(counter=1)


if __name__ == '__main__':
    app.run()
