#!/usr/bin/env python3

#export SLACK_BOT_TOKEN=Bot User OAuth Access Token
#export API_KEY=Weather API Key;

import os
import time
import re
import io
import sys
import urllib.request
from slackclient import SlackClient

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

weather_api_key = os.environ.get('API_KEY')

#list is used for fixing typos
city_list = [ ]
#dict is used to store ID once we found the city
city_dict = { }

MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return matches.group(2).strip() if matches else None


#used to find distance between two strings
#used in a loop with correct to autocorrect words
#returns an int with distance from the two strings
def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]
	
#try to correct city based on the city list 
#returns the closest city by name
def correct(word):
	min_dist = sys.maxsize
	closest_word = None
	for city in city_list:
		dist = levenshtein(city, word)
		if dist < min_dist:
			min_dist = dist
			closest_word = city

	return closest_word

	
#poor man's NLP. It works!
#return tuple(if this is a weather string, where to split the string)
def is_weather_request(sentence):
	sentence = sentence.lower()
	max_distance = 16

	if levenshtein("whats the weather in", sentence) < max_distance:
		return (True,4)
	
	if levenshtein("whats weather in", sentence) < max_distance or levenshtein("whats weather for", sentence) < max_distance:
		return (True, 3)
	
	if levenshtein("weather in", sentence) < max_distance or levenshtein("weather for", sentence) < max_distance:
		return (True,2)
	
	if levenshtein("weather", sentence) < max_distance:
		return (True,1)

	return (False,0)
	
#split sentence to get city
#returns city name minus question mark at the end
def get_location(sentence, split_loc):

	#remove question mark
	if sentence[len(sentence)-1] == '?':
		sentence = sentence[:-1]

	#split string
	split = sentence.split(' ')[split_loc:]

	return " ".join(split)	

#actually request the data 
#returns string with current conditions
def request(city):
	if not (city in city_dict):
		city = correct(city)

	with urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?id=' + str(city_dict[city]) + '&units=metric&appid=' + weather_api_key) as url:
		data = json.loads(url.read().decode())
		return "Current weather in " + city + " is " + data["weather"][0]["description"] + " at " + str(data["main"]["temp"]) + "C"

#process the message
def process_message(msg_echo):
	for update in msg_echo:
		print('Update found...')
		if 'type' in update and update['type'] == 'message':
			message = parse_direct_mention(update["text"])
			
			(is_req, split) = is_weather_request(message)
			
			#if we're a request, change message to weather
			if is_req:
				city_name = get_location(message, split)
				message = request(city_name)
				
			slack_client.rtm_send_message(update["channel"], message)
	
			
def main():
	#read in city list
	with open('city.list.json', mode="r", encoding="utf-8") as f:
		json_cities = json.load(f)
	
	#create a dictionary of cities for id, and a list for corrections
	for city in json_cities:
		city_dict[city["name"]] = city["id"]
		city_list.append(city["name"])


    if slack_client.rtm_connect():
        print('RepeaterBot has gone online...')
        while True:
            msg_echo = slack_client.rtm_read()
            print(msg_echo)
            process_message(msg_echo)
            time.sleep(1)
    else:
        print("Connection Failed...")

if __name__ == '__main__':
    main()
