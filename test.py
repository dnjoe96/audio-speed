API_KEY='782ad5e3c67d4aaa9844057332d0591e'

import requests

auth_key = '782ad5e3c67d4aaa9844057332d0591e'
headers = {"authorization": auth_key, "content-type": "application/json"}


def read_file(filename):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(5242880)
            if not data:
                break
            yield data


upload_response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers,
                                data=read_file('test_audio.mp3'))
audio_url = upload_response.json()["upload_url"]

transcript_request = {'audio_url': audio_url}
transcript_response = requests.post("https://api.assemblyai.com/v2/transcript",
                                    json=transcript_request, headers=headers)
_id = transcript_response.json()["id"]

print(transcript_response.json())