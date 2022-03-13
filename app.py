#!/usr/bin/env python3
import click
import json
import requests

# eventually, I would have to call getenv from the environment
auth_key = '782ad5e3c67d4aaa9844057332d0591e'
endpoint = "https://api.assemblyai.com/v2/transcript"

headers = {
    "authorization": auth_key,
    "content-type": "application/json"
}


def is_link(string):
    if string is None:
        return False
    if 'http://' in string or 'https://' in string:
        return True
    else:
        return False


def read_file(filename):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(5242880)
            if not data:
                break
            yield data


def link_handler(link):
    json = {
        "audio_url": link
    }
    response = requests.post(endpoint, json=json, headers=headers)
    print('url posted')
    return response.json()


def media_file_handler(file):
    # with this url, we upload audio file
    upload_response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers,
                                    data=read_file('test_audio.mp3'))
    print('file uploaded')
    audio_url = upload_response.json()["upload_url"]

    return link_handler(audio_url)


def get_result(_id, status):
    headers = {"authorization": auth_key}
    endpoint = "https://api.assemblyai.com/v2/transcript/{}".format(_id)
    response = requests.get(endpoint, headers=headers)

    print('processing .', end="")
    while status != 'completed':
        print('.', end="")
        response = requests.get(endpoint, headers=headers)
        status = response.json()['status']
    print('\ndone')
    return len(response.json()['words']), response.json()['audio_duration']


supported_files = ".3ga .aac .ac3 .aif .aiff .alac .amr .ape .au .dss .flac " \
                  ".flv .m4a .m4b .m4p .mp3 .mpga .ogg, .oga, .mogg .opus .qcp " \
                  ".tta .voc .wav .wv"

_help = 'pass audio file in the format\n' \
        '-f [filename | link-url] ' \
        '\t audio file or audio url (http).\n' \
        '\t Supported file formats are: \n \t' + supported_files


@click.command()
# @click.argument('audio_file')
@click.option('-f', '--file', default=None, help=_help)
def getspeed(file):
    if file is None:
        click.echo(_help)
        return
    if is_link(file):
        response = link_handler(file)
    else:
        response = media_file_handler(file)

    res = get_result(response['id'], response['status'])
    click.echo(res)


if __name__ == '__main__':
    getspeed()
