#Tutorial: consuming Twitter’s real-time stream API in Python | Ars Technica
#http://arstechnica.com/information-technology/2010/04/tutorial-use-twitters-new-real-time-stream-api-in-python/
####################################################################################################################
#DESCRIPTION:
#--------------
#	The easiest way to handle HTTP streaming in Python is to use PyCurl, the 
#	Python bindings for the well-known Curl network library. PyCurl allows 
#	you to provide a callback function that will be executed every time a 
#	new block of data is available. The following code is a simple 
#	demonstration of HTTP streaming with PyCurl: (see below)
#
#############################################################################################################################################################
#TwitterAPI website: https://github.com/geduldig/TwitterAPI
#https://dev.twitter.com/docs/api/1.1/get/search/tweets
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRestPager
from datetime import datetime
import sys
import os
import csv

#############################################################################################################################################################
#Variables:

dict_hashtag = {
	'tag_1': 'edtech',
	'tag_2': 'CatchingFire',
	'tag_3': 'EndersGame',
	'tag_4': 'LastVegas',
	'tag_5': 'ThorDarkWorld',
}

twitter_hashtag = dict_hashtag['tag_3']
data_folder = "Twitter Data"	#Folder where data should be stored

dir = sys.path[0]
write_folder = os.path.join(dir, data_folder)
filepath = os.path.join(write_folder, twitter_hashtag + ".csv")
loop_counter_break = 0
LOOP_BREAK_NUMBER = 101

data_lst = []
TEST_NUMBER = 5

#############################################################################################################################################################
#Functions:
def writeMyTweet(filepath, data_lst):
	# Have we seen that Tweet before, and saved it?
	newTweet = False
	#try:
	#	f = open(filepath, 'r')
	#	fileTweet = f.read();
	#	if fileTweet != twitterTweet:
	#		newTweet = True
	#	f.close()
	#except IOError:
	#	newTweet = True # file not present, make new file with current tweet
	 
	# if new, overwrite old file with new tweet and send email alert
	#if newTweet:
	#	with open(filepath, 'w') as f:
	#		f.write(twitterTweet.decode())
	#If the file already exists --> we don't want to re-write the header information
	if os.path.exists(filepath):
		bool_writeheader = False
	else:
		bool_writeheader = True
	
	header_names = ['tweet_id', 'tweet_date', 'user_name', 'user_screen_name', 'tweet_text']
	target = open(filepath, 'ab')
	target_csv = csv.DictWriter(target, 
		fieldnames = header_names, delimiter=',', quoting=csv.QUOTE_MINIMAL)
	#target_csv = csv.DictWriter(target, 
	#	fieldnames = data_lst[0].keys(), delimiter=',', quoting=csv.QUOTE_MINIMAL)
	if bool_writeheader:
		target_csv.writeheader()
	target_csv.writerows(data_lst)
	target.close()
	
	#fieldnames = ['tweet_date', 'tweet_id', 'tweet_date', 
	#		dict_temp['tweet_id'] = item['id_str']
	#		dict_temp['tweet_date'] = item['created_at']
	#		dict_temp['user_name'] = item['user']['name']
	#		dict_temp['user_screen_name'] = item['user']['screen_name']
	#		dict_temp['tweet_text'] = item['text']
	return
	
#############################################################################################################################################################
#############################################################################################################################################################
# SAVE YOUR APPLICATION CREDENTIALS IN TwitterAPI/credentials.txt.
o = TwitterOAuth.read_file()
api = TwitterAPI(o.consumer_key, o.consumer_secret, o.access_token_key, o.access_token_secret)



try:
	if TEST_NUMBER == 0:

		# VERIFY YOUR CREDS
		r = api.request('account/verify_credentials')
		print(r.text)

	if TEST_NUMBER == 1:

		# POST A TWEET 
		r = api.request('statuses/update', {'status':'the time is now %s' % datetime.now()})
		print(r.status_code)

	if TEST_NUMBER == 2:

		# GET 5 TWEETS CONTAINING 'ZZZ'
		for item in api.request('search/tweets', {'q':'zzz', 'count':5}):
			print(item['text'] if 'text' in item else item)

	if TEST_NUMBER == 3:

		# STREAM TWEETS FROM AROUND NYC
		for item in api.request('statuses/filter', {'locations':'-74,40,-73,41'}):
			print(item['text'] if 'text' in item else item)

	if TEST_NUMBER == 4:
		# GET TWEETS FROM THE PAST WEEK OR SO CONTAINING 'LOVE'
		pager = TwitterRestPager(api, 'search/tweets', {'q':'CatchingFire'});	
		#for item in pager.get_iterator():
		#	print(item['text'] if 'text' in item else item)

	if TEST_NUMBER == 5:
	# GET TWEETS FROM THE PAST WEEK OR SO CONTAINING 'LOVE'
		my_request_param_dict = {
			'q': '%23' + twitter_hashtag,
		}
		pager = TwitterRestPager(api, 'search/tweets', my_request_param_dict);
		for item in pager.get_iterator():
			#print item['id_str']
			a = item
			print "%d - %s" % (loop_counter_break, item['user']['name'],)
			try:
				dict_temp = {
					'tweet_id': item['id_str'].encode(), 
					'tweet_date': item['created_at'].encode(),
					'user_name': item['user']['name'].encode(),
					'user_screen_name': item['user']['screen_name'].encode(),
					'tweet_text': item['text'].encode(),
				}
			except Exception as e:
				print "Error - exception"
				continue
			data_lst.append(dict_temp)
			loop_counter_break += 1
			if loop_counter_break >= LOOP_BREAK_NUMBER:
				break
except Exception as e:
	print(e)
	
	
writeMyTweet(filepath, data_lst)

		
#############################################################################################################################################################

#############################################################################################################################################################

if 1 < 0:
	#pager = TwitterRestPager(api, 'search/tweets', my_request_param_dict); 
	pager.params	#returns: my_request_param_dict; e.g. {'q': '%23CatchingFire', 'util': '2013-10-06'}

if 1 < 0:
	for item in pager.get_iterator():
		a = item
		break
	for item in a.keys():
		print item
	item['text']
	item['id_str']	#tweet id (unique to tweet)
	item['created_at']	#Date: (e.g: Sun Oct 06 19:52:39 +0000 2013)
	item['user']['id'] #user id
	#User post: item['user']['name'] @item['user']['screen_name']
	item['user']['screen_name'] #screen name (e.g. @katnissevadank)
	item['user']['name'] #Name (bold letters before the 'screen_name')
	itema['user']['lang'] #Language post is in (e.g. en = English)
	item['user']['created_at'] #Date User Profile was Created (e.g. Wed Sep 14 23:37:06 +0000 2011)
	item['user']['time_zone'] #time zone selected by user (e.g. Arizona)
	
#############################################################################################################################################################
	
	

