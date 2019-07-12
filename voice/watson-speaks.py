from __future__ import print_function
import json
from os.path import join, dirname
from ibm_watson import TextToSpeechV1
from ibm_watson.websocket import SynthesizeCallback
service = TextToSpeechV1(
    ## url is optional, and defaults to the URL below. Use the correct URL for your region.
    url='https://stream.watsonplatform.net/text-to-speech/api',
iam_apikey='VcK77_raDyYJJMOPw4zchX_4Sowc3ToBmgo3MQjmvaLH')


data_text = 'Charlie, eat a dick.'

with open('output.wav','wb') as audio_file:
    response = service.synthesize(data_text, accept='audio/wav',voice="en-US_AllisonVoice").get_result()
    audio_file.write(response.content)


