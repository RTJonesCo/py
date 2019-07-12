import sys
import os
import sys
import time
import datetime


#
#hack to make the imports work correct
#print("adding libs to sys.path")
#sys.path.append("/home/pi/.local/lib/python3.7/site-package")
#print("debug:\t showing sys.path")
#print(sys.path)
#

import feedparser
import pickle
from pygame import mixer



code = "r3vd2ad"
interval = 1
last_run  = "empty"
DATA_FILE = "last_run_data.obj"
music_index = ['alert-tone.wav','default-tone.mp3','leroy.mp3','applause-1.wav' ]
alert_file ="empty"
mixer.init()
music_index_len = len(music_index)
department_name = "empty"
BASE_DIR = "/home/pi/code/active911_project/"
#

#
print("debug:\t running in dir " + os.getcwd())

print("debug:\tsound subsystem loaded, loaded " + str(music_index_len)+", selected idx:0")

alert_file = music_index[0]

#url="https://feeds2.feedburner.com/TheGeeksOf3d"
if len(sys.argv) == 2:
	code = sys.argv[1]
	print("debug:\tfound command line code: " + code)
	alert_file = music_index[0]
	print(music_index)
if len(sys.argv) ==3:
	code= sys.argv[1]
	print("debug:\tfound command line code: " + code)
	arg = sys.argv[2]
	print("debug:\tselected music idx: " + arg)
	music_idx = int(arg)
	if music_idx <= music_index_len:
		alert_file = music_index[music_idx]

mixer.music.load(BASE_DIR + alert_file)

#inital load then loop it
url="https://access.active911.com/interface/rss.php?"+code
	
feed_deptname = feedparser.parse(url)
	#print("loading feed....\n")
	#for post in feed.entries:
department_name = feed_deptname.feed.title
print("********** " + department_name + " **********")
while True:
#	print(datetime.datetime.now().time())
#	print("using code [ " + code + "]")
	#url="https://access.active911.com/interface/rss.php?"+code
	
	feed = feedparser.parse(url)
	#print("loading feed....\n")
	#for post in feed.entries:
	#department_name = feed.feed.title
	#print("********** " + department_name + " **********")
	
	
	post = feed['entries'][0]
#	date = "(%d/%02d/%02d)" % (post.published_parsed.tm_year, post.published_parsed.tm_mon, post.published_parsed.tm_mday)
	date = post.published
	run_text = date + "\t" +post.title+ "\t\t" + post.description
	
	if (last_run != run_text):
		
		mixer.music.play()
		#print("********** " + department_name + " **********\n")
		print("\n########## NEW CALL ##########")
		print(run_text)
		last_run = run_text
		data_file = open(DATA_FILE,'wb')
		pickle.dump(last_run,data_file)
		print(datetime.datetime.now().time())
		time.sleep(interval)
		
		
