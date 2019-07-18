import sys
import os
import sys
import time
import datetime
import argparse
import logging


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

# croft code = "r3vd2ad"
# duncan code ="r3vd1np"
code = 'r3vd1np'
interval = 1
last_run  = "empty"
DATA_FILE = "last_run_data.obj"
music_index = ['alert-tone.wav','default-tone.mp3','leroy.mp3','applause-1.wav' ]
alert_file ="empty"
mixer.init()
music_index_len = len(music_index)
department_name = "empty"
if os.name == "linux":
	BASE_DIR = "/home/pi/code/active911_project/"
	
if os.name=="nt":
	BASE_DIR = "C:\\code\\active911\\"
		
logging.debug("working dir " + BASE_DIR)


def initilize():
	global code 
	global alert_file
	global interval
	#('-s', action='store', dest='simple_value',
	#setup logger
	logging.basicConfig(filename='active911.log', filemode='w', level=logging.DEBUG)
	#check the command line for options
	parser = argparse.ArgumentParser(description='Connect to an active 911 feed, and monitor it for alerts')
	parser.add_argument('--code',action='store',dest='code',default='r3vd1np',help='set the active911 rss feed code')
	parser.add_argument('--alert',action='store',dest='alert',type=int,help='set the active alert tone')
	parser.add_argument('--interval',action='store',dest='interval',type=int,default=1,help='set the sleep time of the loop in seconds')

	parser.add_argument('--version', action='version', version='%(prog)s 1.0')
	logging.debug("command line args")
	args = parser.parse_args()
	logging.debug(args)
	interval = args.interval
	code = args.code
	music_idx = int(args.alert)
	if music_idx <= music_index_len:
		alert_file = music_index[music_idx]
	else:
		alert_file = music_index[0]
	mixer.music.load(BASE_DIR + alert_file)


initilize()
logging.debug("current running dir " + os.getcwd())
logging.debug("sound subsystem initilized")
logging.debug("found " + str(music_index_len) + " alert files")
logging.debug("selected idx:0")
logging.debug("initilize complete")

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