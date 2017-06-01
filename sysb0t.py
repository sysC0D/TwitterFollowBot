#!/usr/bin/pythoni3

from TwitterFollowBot import TwitterBot
from twitter import *
from time import sleep
import sys
import random

# Get Trends from Twitter
def get_trends(woeid, maxhash):
	in_file = open("config.txt", "r")
	bot_conf = {}
	for line in in_file:
		line = line.split(":")
		parameter = line[0].strip()
		value = line[1].strip()
		bot_conf[parameter] = value

	twitter = Twitter(
		auth = OAuth(bot_conf["OAUTH_TOKEN"], bot_conf["OAUTH_SECRET"], bot_conf["CONSUMER_KEY"], bot_conf["CONSUMER_SECRET"]))

	results = twitter.trends.place(_id = woeid)
	
	hashlist = []
	for location in results:
		for trend in location["trends"]:
			if maxhash > 0:
				hashlist.append(trend["name"])
				maxhash-=1
	return hashlist


# Sync Twitter
print("---Init Session")
sysbot = TwitterBot('config.txt')
sysbot.sync_follows()

count=0
while (count < 500):
	print("---Start Session")
	sys.stdout.flush()
	# Get trend (hashtag & name)
	#-----------------------------------------------------------------------
	# retrieve global trends.
	# http://woeid.rosselliot.co.nz/
	#-----------------------------------------------------------------------
	hashtags = get_trends(615702, 20)
	listhash = []
	listname = []

	for tag in hashtags:
		if tag.find("#") != -1 :
			listhash.append(tag)
		else :
			listname.append(tag)

	# Select subject
	selecthash=random.choice(listhash)
	selectname=random.choice(listname)

	# RT and like
	sysbot.auto_rt(selecthash, count=2)
	sysbot.auto_fav(selectname, count=3)

	# Follow
	sysbot.auto_follow(selecthash, count=2)

	#Wait next session
	waitnextsession=random.randrange(0, 120, 7)
	sleep(waitnextsession)

	#Mute following
	sysbot.auto_mute_following()

	count+=1
	print("---End Session")
	sys.stdout.flush()

# Clean No follower
sysbot.auto_unfollow_nonfollowers()
