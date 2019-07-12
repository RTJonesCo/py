from __future__ import print_function
import feedparser
import sys
import time
import pickle
from pygame import mixer

#from __future__ import print_function
import json
from os.path import join, dirname
from ibm_watson import TextToSpeechV1
from ibm_watson.websocket import SynthesizeCallback
service = TextToSpeechV1(
    ## url is optional, and defaults to the URL below. Use the correct URL for your region.
    url='https://stream.watsonplatform.net/text-to-speech/api',
iam_apikey='VcK77_raDyYJJMOPw4zchX_4Sowc3ToBmgo3MQjmvaLH')




 
code = "r3vd2ad"
interval = 1
last_run  = "empty" 
DATA_FILE = "last_run_data.obj"
music_index = ['leroy.mp3','applause-1.wav','open-door.wav','moaning.wav' ]
alert_file ="empty" 
mixer.init()
music_index_len = len(music_index)
department_name = "empty" 
#mixer.music.load('leroy.mp3')
#music_index[0] = 'leroy.mp3'

#mixer.music.load('applause-1.wav')
#music_index[1] = 'applause-1.wav'

print("sound subsystem loaded, loaded " + str(music_index_len))

alert_file = music_index[0]

#url="https://feeds2.feedburner.com/TheGeeksOf3d"
if len(sys.argv) == 2:
	code = sys.argv[1]
	print("found command line code: " + code)
	alert_file = music_index[0]
	print(music_index)
if len(sys.argv) ==3:
	code= sys.argv[1]
	print("found command line code: " + code)
	arg = sys.argv[2]
	music_idx = int(arg)
	if music_idx <= music_index_len:
		alert_file = music_index[music_idx]

#temp -> put me back mixer.music.load(alert_file)
while True:
	
#	print("using code [ " + code + "]")
	url="https://access.active911.com/interface/rss.php?"+code
	
	feed = feedparser.parse(url)
	#print("loading feed....\n")
	#for post in feed.entries:
	department_name = feed.feed.title
	
	
	post = feed['entries'][0]
#	date = "(%d/%02d/%02d)" % (post.published_parsed.tm_year, post.published_parsed.tm_mon, post.published_parsed.tm_mday)
	date = post.published
	run_text = date + "\t" +post.title+ "\t\t" + post.description
#	print("run_text: " + run_text)
	
	if (last_run != run_text):
		# after file is made mixer.music.play()
		#so far this shit doesnt work right, so spawn a background process to build and then play the file while the app updates 
		with open('output.wav','wb') as audio_file:
    			response = service.synthesize(run_text, accept='audio/wav',voice="en-US_AllisonV3Voice",timings={run_text}).get_result()
    			audio_file.write(response.content)
		#time.sleep(5)
		#mixer.music.play()
		mixer.music.load('output.wav')
		#mixer.music.queue('output.wav')
		mixer.music.play()
		print("********** " + department_name + " **********")
		print("\n########## NEW CALL ##########") 
		print(run_text)
		
		
		last_run = run_text
		data_file = open(DATA_FILE,'wb')
		pickle.dump(last_run,data_file)
		time.sleep(interval)
		
		


