# TODO: Get a message, compress it using the fano-shanon algorithm, encode the result using linear code
# TODO: and random noise and send it to the server for decoding as a json


# send something to the server in http://127.0.0.1:5000

import requests

# Sending a GET request
response = requests.get('http://127.0.0.1:5000/')
print(f'GET Response: {response.text}')

# Sending a POST request with JSON data
data = {'key': 'value'}
response = requests.post('http://127.0.0.1:5000/post', json=data)
print(f'POST Response: {response.json()}')
