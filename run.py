import sys
import os
import sys
import time
import datetime
import argparse
import logging
import json

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

logging.basicConfig(filename='active911.log',filemode='w',
        level=logging.DEBUG,
        format='%(asctime)s\t%(levelname)s\t%(threadName)-10s\t%(message)s',)

	

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
CONFIG_FILE = 'config.json'
if os.name == "linux":
	BASE_DIR = "/home/pi/code/active911_project/"
	
if os.name=="nt":
	BASE_DIR = "C:\\code\\active911\\"

logging.debug("working dir " + BASE_DIR)



def save_config(code="r3vd1np",interval=1,alert="alert-tone.wav",last_run=""):
	logging.debug("saving config")
	config = {
		'code': code,
		'interval' : interval,
		'alert' : alert,
		'last_run' : last_run
	}
	logging.debug(config)
	with open(CONFIG_FILE, 'w') as f:  # writing JSON object
		json.dump(config, f)
		logging.debug('config file saved..')

def load_config():
	logging.debug("Loading Config")
	config = json.load(CONFIG_FILE)
	logging.debug(config)
	return config

def load_alert_from_dir():
	logging.debug("loading alerts from alerts dir")
	#print("debug:\tloading alerts from alerts dir")

	directory = os.fsencode(BASE_DIR + "alerts")
	logging.debug("looking for alerts " + BASE_DIR + "alerts")
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		if filename.endswith(".wav") or filename.endswith(".mp3"): 
        	# print(os.path.join(directory, filename))
			logging.debug("found alert file:\t" + os.path.join(directory, filename))
			#print("debug:\tfound alert file:\t" + os.path.join(directory, filename))
			
	else:
		logging.debug("no alert files found")
		#print("debug:\tno alert files found in alerts folder")

def initilize():
	global code 
	global alert_file
	global interval
	music_idx = 0
	#('-s', action='store', dest='simple_value',
	#setup logger
	
	
	
	#check the command line for options
	parser = argparse.ArgumentParser(description='Connect to an active 911 feed, and monitor it for alerts')
	parser.add_argument('--code',action='store',dest='code',default='r3vd1np',help='set the active911 rss feed code')
	parser.add_argument('--alert',action='store',dest='alert',help='set the active alert tone')
	parser.add_argument('--interval',action='store',dest='interval',type=int,default=1,help='set the sleep time of the loop in seconds')

	parser.add_argument('--version', action='version', version='%(prog)s 1.0')
	#load any extra alerts
	load_alert_from_dir()
	#load the config overwrite default app settings 
	config = load_config()
	#
	logging.debug("command line args")
	args = parser.parse_args()
	logging.debug(args)
	interval = args.interval
	code = args.code
	
	if args.alert is not None:
		music_idx = int(args.alert)
		if music_idx <= music_index_len:
			alert_file = music_index[music_idx]
		else:
			alert_file = music_index[music_idx]
		mixer.music.load(BASE_DIR + alert_file)

	else:
		alert_file = music_index[0]
		mixer.music.load(BASE_DIR + alert_file)




if __name__ == "__main__":
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
save_config()
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