import requests
import json as jjson
import time

_maxNumRetries = 10

def processRequest(api, json, data, headers, params):
    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request('post', api, json=json, data=data, headers=headers, params=params)

        print ('POST', response)

        if response.status_code == 429:

            print("Message: %s" % (response.json()['error']['message']))

            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content

        elif response.status_code == 202:

            url = response.headers['Operation-Location']

            tries = 0
            response = requests.request('get', url, json=json, data=data, headers=headers, params=params)
            print('GET', response, response.json()['status'])
            print_json(response)
            while tries < _maxNumRetries and response.json()['status'] == 'Running':
                tries +=1
                response = requests.request('get', url, json=json, data=data, headers=headers, params=params)
                print('GET', response, response.json()['status']); print_json(response)
                time.sleep(10)
                if response.json()['status'] == 'Succeeded':
                    result = response.json()['processingResult']
            if tries >= _maxNumRetries:
                print("ERROR: Too many tries on 202 video processing.")
                exit(1)

        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()['error']['message']))
            exit(1)

        break

    return result


def print_json(response):
    print(jjson.dumps(jjson.loads(response.text), indent=4))