    # TODO: Get a message, compress it using the fano-shanon algorithm, linear_code the result using linear code
# TODO: and random noise and send it to the server for decoding as a json


# send something to the server in http://127.0.0.1:5000

import requests
import random as rand

# Sending a GET request
response = requests.get('http://127.0.0.1:5000/')
print(f'GET Response: {response.text}')

# Sending a POST request with JSON data
data = {'key': 'value'}
response = requests.post('http://127.0.0.1:5000/post', json=data)
print(f'POST Response: {response.json()}')

# Changes random digits on the data that have been processed through fanon-shannon compression algorithm and linear code for error checking.
#The data are inside a list of ints of values 0 or 1
def applyNoise(data):
    for i in data:
        if (rand.randint(0,30)==1):
            if (i==1):
                i=0
            elif (i==0):
                i=1
    return data