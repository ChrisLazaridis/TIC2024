from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

# TODO: get the message, decode it using the linear code, decompress it using the fano-shanon algorithm
# TODO: and print the result
