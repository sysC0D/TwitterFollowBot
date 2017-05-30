#!/usr/bin/python

from TwitterFollowBot import TwitterBot
from twitter import *

#Get Trends from Twitter
def get_trends():
        #Load Credential
	in_file = open("config.txt", "r")
	bot_conf = {}
	for line in in_file:
		line = line.split(":")
		parameter = line[0].strip()
		value = line[1].strip()
		bot_conf[parameter] = value

	twitter = Twitter(
		auth = OAuth(bot_conf["OAUTH_TOKEN"], bot_conf["OAUTH_SECRET"], bot_conf["CONSUMER_KEY"], bot_conf["CONSUMER_SECRET"]))


        #-----------------------------------------------------------------------
        # retrieve global trends.
        # http://woeid.rosselliot.co.nz/
        #-----------------------------------------------------------------------
	results = twitter.trends.place(_id = 615702)
	
	hashlist = []
	maxhash = 5
	for location in results:
		for trend in location["trends"]:
			if trend["name"].find("#") != -1 :
				if maxhash > 0:
					hashlist.append(trend["name"])
					maxhash-=1
	return hashlist



sysbot = TwitterBot('config.txt')
hashtags = get_trends() 
 
for tag in hashtags:
	print(tag)
#	print(i)
#   	#my_bot.auto_rt(i, count=3)
#   	time.sleep(60)
