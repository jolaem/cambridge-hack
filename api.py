import requests
import json as jjson
import time

_maxNumRetries = 10

_url_face = 'https://api.projectoxford.ai/face/v1.0/detect'
_url_emotion = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
#_face_key = "576ef033c83d4dc2b27cd1480129ecae"
_face_key = "2b80fddffaa14b859679d3faafe3d1b1"
#_emotion_key = "1fb3192517d04f36b73690f1170caa81"
_emotion_key = "96b5e8dc481c483a9a7d158ba10b1e17"

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

def get_faces_frame(img):

    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _face_key
    headers['Content-Type'] = 'application/octet-stream'

    params = dict()
    params['returnFaceId'] = 'true'
    params['returnFaceLandmarks'] = 'true'
    params['returnFaceAttributes'] = 'age'

    json = None
    data = img

    result = processRequest(_url_face, json, data, headers, params)
    #print("RESULTS:")
    #print(jjson.dumps(result, indent=4))

    return result

def get_emotions_frame(img):
    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _emotion_key
    headers['Content-Type'] = 'application/octet-stream'

    json = None
    params = None
    data = img

    result = processRequest(_url_emotion, json, data, headers, params)

    #print("RESULTS:")
    #print(jjson.dumps(jjson.loads(result), indent=4))

    return result