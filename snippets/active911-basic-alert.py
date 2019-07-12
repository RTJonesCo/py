import feedparser
import sys
import time
from pygame import mixer
 
code = "r3vd2ad"
interval = 1
last_run  = "empty" 

mixer.init()

mixer.music.load('leroy.mp3')
mixer.music.load('applause-1.wav')

print("sound subsystem loaded")


#url="https://feeds2.feedburner.com/TheGeeksOf3d"
if len(sys.argv) == 2:
	code = sys.argv[1]
	print("found command line code: " + code)



while True:
	
#	print("using code [ " + code + "]")
	url="https://access.active911.com/interface/rss.php?"+code

	feed = feedparser.parse(url)
	#print("loading feed....\n")
	#for post in feed.entries:
	post = feed['entries'][0]
#	date = "(%d/%02d/%02d)" % (post.published_parsed.tm_year, post.published_parsed.tm_mon, post.published_parsed.tm_mday)
	date = post.published
	run_text = date + "\t" +post.title+ "\t\t" + post.description
#	print("run_text: " + run_text)

	if (last_run != run_text):
		mixer.music.play(0)
		print("\n########## NEW CALL ##########") 
		print(run_text)
		last_run = run_text
		time.sleep(interval)
		
		


