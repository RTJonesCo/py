import feedparser
import sys
import time
 
code = "r3vd2ad"

#url="https://feeds2.feedburner.com/TheGeeksOf3d"
if len(sys.argv) == 2:
	code = sys.argv[1]
	print("found code: " + code)


while True:
	url="https://access.active911.com/interface/rss.php?"+code

	feed = feedparser.parse(url)
	print("loading feed....\n")
	for post in feed.entries:
		date = "(%d/%02d/%02d)" % (post.published_parsed.tm_year, post.published_parsed.tm_mon, post.published_parsed.tm_mday)
		print( date + " { " + post.title + " } " + "[ " + post.description + " ]")
#		print("title: " + post.title)
	
	time.sleep(5)


