from flask import Flask, jsonify
from store import redis


app = Flask(__name__)


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
