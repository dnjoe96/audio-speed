import json

import requests
from test import auth_key

endpoint = "https://api.assemblyai.com/v2/transcript"
# json = {
#     "audio_url": "test_audio.mp3"
# }
headers = {
    "authorization": auth_key,
    "content-type": "application/json"
}


def read_file(filename):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(5242880)
            if not data:
                break
            yield data


# with this url, we upload audio file
upload_response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers,
                                data=read_file('test_audio.mp3'))
audio_url = upload_response.json()["upload_url"]

transcript_request = {'audio_url': audio_url}
transcript_response = requests.post("https://api.assemblyai.com/v2/transcript",
                                    json=transcript_request, headers=headers)
# print(transcript_response.json())

_id = transcript_response.json()["id"]

endpoint = "https://api.assemblyai.com/v2/transcript/{}".format(_id)
# print(endpoint)

# print('===========================')

headers = {
    "authorization": auth_key,
}

reponse_status = transcript_response.json()['status']
while reponse_status != 'completed':
    # print(reponse_status)
    response = requests.get(endpoint, headers=headers)
    reponse_status = response.json()['status']


print(json.dumps(response.json(), indent=2))
# print(response.json())
