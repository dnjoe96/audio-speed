import click
import json
import requests
from test import auth_key

auth_key = '782ad5e3c67d4aaa9844057332d0591e'
endpoint = "https://api.assemblyai.com/v2/transcript"



"""
endpoint = "https://api.assemblyai.com/v2/transcript"
json = {
    "audio_url": "https://bit.ly/3yxKEIY"
}
headers = {
    "authorization": "YOUR-API-TOKEN",
    "content-type": "application/json"
}
response = requests.post(endpoint, json=json, headers=headers)
print(response.json())


############# GET RESULT ##################
import requests
endpoint = "https://api.assemblyai.com/v2/transcript/YOUR-TRANSCRIPT-ID-HERE"
headers = {
    "authorization": "YOUR-API-TOKEN",
}
response = requests.get(endpoint, headers=headers)
print(response.json())

"""


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




supported_files = ".3ga .aac .ac3 .aif .aiff .alac .amr .ape .au .dss .flac " \
                  ".flv .m4a .m4b .m4p .mp3 .mpga .ogg, .oga, .mogg .opus .qcp " \
                  ".tta .voc .wav .wv"

_help = 'audio file or audio url (http).\n' \
        'Supported file formats are: \n ' + supported_files


@click.command()
# @click.argument('audio_file')
@click.option('-f', '--file', default=None, help=_help)
def getspeed(file):
    click.echo('Hello World!' + file)


if __name__ == '__main__':
    getspeed()
    # print(help_file)