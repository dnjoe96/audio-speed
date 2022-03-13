#!/usr/bin/env python3
import os
import click
import requests
from time import sleep


auth_key = os.environ.get('AUTH_KEY')
endpoint = "https://api.assemblyai.com/v2/transcript"

headers = {
    "authorization": auth_key,
    "content-type": "application/json"
}


def is_link(string):
    """
        function to check if a string is a url link
    :param string:
    :return: Boolean - True or False
    """
    if string is None:
        return False
    if 'http://' in string or 'https://' in string:
        return True
    else:
        return False


def read_file(filename):
    """
        Reads a file and returns the output as a stream
    :param filename:
    :return: stream
    """
    try:
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(5242880)
                if not data:
                    break
                yield data
    except FileNotFoundError as e:
        print(e)
        exit(1)


def link_handler(link):
    """
        Using the audio link, this functions makes a call to the
        transcript API
    :param link:
    :return: Http response
    """
    json = {
        "audio_url": link
    }

    try:
        response = requests.post(endpoint, json=json, headers=headers)
    except Exception as e:
        print(e)
        exit(1)

    print('url posted')
    # print(response.status_code)
    return response


def media_file_handler(file):
    """
        The function uploads a media file into the Assembly AI Upload API
    :param file:
    :return: http response
    """
    upload_response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers,
                                    data=read_file(file))
    if upload_response.status_code != 200:
        return upload_response
    print('file uploaded')
    audio_url = upload_response.json()["upload_url"]

    return link_handler(audio_url)


def get_result(_id, status):
    """
        This function checks the result after the API transcription
        for error or completion
    :param _id: if of the transcript json responnse
    :param status: status of the transcription
    :return: Tuple - word count and audio duration
    """
    # print('processing')
    headers = {"authorization": auth_key}
    endpoint = "https://api.assemblyai.com/v2/transcript/{}".format(_id)

    try:
        response = requests.get(endpoint, headers=headers)
    except Exception as e:
        print(e)
        exit(1)

    while status not in ['completed', 'error']:
        sleep(5)
        print(status)
        response = requests.get(endpoint, headers=headers)
        status = response.json()['status']
    print('done')

    if status == 'error':
        return response.json()['error']
    return len(response.json()['words']), response.json()['audio_duration']


supported_files = ".3ga .aac .ac3 .aif .aiff .alac .amr .ape .au .dss .flac " \
                  ".flv .m4a .m4b .m4p .mp3 .mpga .ogg, .oga, .mogg .opus .qcp " \
                  ".tta .voc .wav .wv"

_help = 'pass audio file in the format\n' \
        '-f [filename | link-url] ' \
        '\t audio file or audio url (http).\n' \
        '\t Supported file formats are: \n \t' + supported_files


@click.command()
@click.option('-f', '--file', default=None, help=_help)
def getspeed(file):
    if file is None:
        click.echo(_help)
        return
    if is_link(file):
        response = link_handler(file)
    else:
        response = media_file_handler(file)

    if response.status_code != 200:
        res = response.json()['error']
    else:
        res = get_result(response.json()['id'], response.json()['status'])
    # click.echo(res)

    speed = res[0] / (res[1] / 60)
    click.echo('speed is = {:.2f}'.format(float(speed)))
    if speed > 160:
        click.echo("Too fast")
    elif speed < 120:
        click.echo("Too slow")
    else:
        click.echo("Speed ok")


if __name__ == '__main__':
    getspeed()
