from flask import Flask, abort, jsonify, request
import os
from store import redis


app = Flask(__name__)


@app.errorhandler(401)
def unauthorized(e):
    return jsonify(message=str(e)), 401


@app.before_request
def authenticate():
    if 'CAAS-Auth-Token' not in request.headers:
        abort(401)

    if request.headers['CAAS-Auth-Token'] != os.getenv('SECRET_KEY', 'GIAO'):
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


@app.route('/<label>', methods=['DELETE'])
def reset(label):
    counter = redis.delete(label)
    return jsonify(counter=1)


if __name__ == '__main__':
    app.run()
