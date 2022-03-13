# audio-speed

This is a program that measures the speed of speech and notifies whether too fast or too slow.

Using [Assembly AI]('assemblyai.com') async endpoints, this pplication will measure the speakers
speaking rate and notify them if they talk too quickly or slowly.
Greater than 160 words per minute is too fast, and less than 120 is too slow.

This application ia a terminal application.
Therefore, in order to run this application, this repository has to be cloned to your local machine.
---
Requirements
- ubuntu/redhat
- python3

---

clone repo
```commandline
$ git clone git@github.com:dnjoe96/audio-speed.git
```

enter into the repo
```commandline
$ cd audio-speed
```

run the setup script, providing the API auth key from [Assembly AI]('assemblyai.com')
```commandline
audio-speed$ ./script <auth-key>
```

Now your environment is setup with the right dependencies and the authentication key is setup in
the system environment variable. 
- Note: This script has to be run if the system is restarted.

---
Now you can run the script 
```commandline
audio-speed$ ./app.py -f <path to audio file>
```
example
```commandline
audio-speed$ ./app.py -f audiofolder/media.mp3
```
---
or
```commandline
audio-speed$ ./app.py -f <url of audio file>
```
example
```commandline
audio-speed$ ./app.py -f https://facebook.com/some-audo-file
```
---
Here is an test  with an audio file locally
```commandline
(venv) somename@somehost:~/audio-speed$ ./app.py -f audiofolder/media.mp3 
file uploaded
url posted
queued
processing
processing
processing
processing
processing
done
speed is = 135.48
Speed ok
(venv) somename@somehost:~/Desktop/Project25/audio-speed$ 
```
---
### Implementation

I use the GET POST method on the [Assembly AI]('assemblyai.com') API
```python
endpoint = "https://api.assemblyai.com/v2/transcript/"
```

with the POST method, we pass in a json payload containing the audio url
like
```json
{
  'audio_url': 'https://some-url.com'
}
```
to the endpoint and get a json object as response containing keys.
At this stage, my key of interest is the `id`

Because with the `id`, I make a GET request to the same endpoint 
```python
endpoint = "https://api.assemblyai.com/v2/transcript/{}".format(_id)
```

Getting a response of `error` or `completed` means that the request is done
processing and we can analyse the json object to get the return data.

The speed is gotten from
```python
speed =  length-of-words / audio-duration
```

For more information on the modules and API used, here are some resources.
- [Assembly AI docs](https://docs.assemblyai.com/)
- [Click python module](https://click.palletsprojects.com/en/8.0.x/quickstart/)
