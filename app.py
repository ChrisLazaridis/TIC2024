from flask import Flask, request, jsonify
from tests import *
import requests
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/post', methods=['POST'])
def post_example():
    data = request.json
    CompressEncodeDecodeDecomress(str(data[1]))
    return jsonify({'you_sent': data}), 200


if __name__ == '__main__':
    app.run()

# TODO: get the message, decode it using the linear code, decompress it using the fano-shanon algorithm
# TODO: and print the result
