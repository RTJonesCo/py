from __future__ import print_function
import json
from os.path import join, dirname
from ibm_watson import TextToSpeechV1
from ibm_watson.websocket import SynthesizeCallback
service = TextToSpeechV1(
    ## url is optional, and defaults to the URL below. Use the correct URL for your region.
    url='https://stream.watsonplatform.net/text-to-speech/api',
iam_apikey='VcK77_raDyYJJMOPw4zchX_4Sowc3ToBmgo3MQjmvaLH')


# my spaces data_text = 'CROFT LADDER 10:           RESPOND TO A BUSINESS FIRE ALARM,                               , 764 NORTH CHURCH ST., Spartanburg'
#data_text ='CROFT LADDER 10: RESPOND TO A BUSINESS FIRE ALARM,764 N.CHURCH ST.,SPARTANBURG' 
data_text = "YEAHHHHHHAAA BITCH!"
#voices = service.list_voices().get_result()
#print(json.dumps(voices, indent=2))


with open('bs_01.wav','wb') as audio_file:
    response = service.synthesize(data_text, accept='audio/wav',voice="en-US_AllisonV3Voice",timings={data_text}).get_result()
    audio_file.write(response.content)


pronunciation = service.get_pronunciation('Watson', format='spr').get_result()
print(json.dumps(pronunciation, indent=2))

#voice_models = service.list_voice_models().get_result()
#print(json.dumps(voice_models, indent=2))



