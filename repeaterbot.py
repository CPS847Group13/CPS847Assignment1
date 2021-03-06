#!/usr/bin/env python3

#export SLACK_BOT_TOKEN=Bot User OAuth Access Token
#export API_KEY=Weather API Key;

import os
import time
import re
import io
import sys
import json
from slackclient import SlackClient
import urllib2


#instantiate Slack client in main so we don't create a bot for each unit test
slack_client = None 
#same with weather api
weather_api_key = None

#list is used for fixing typos
city_list = [ ]
#dict is used to store ID once we found the city
city_dict = { }

#read in city list
#change to city.list.min.json for all cities
with open('canada.list.min.json', mode="r") as f:
    json_cities = json.load(f)

#create a dictionary of cities for id, and a list for corrections
for city in json_cities:
    city_dict[city["name"]] = city["id"]
    city_list.append(city["name"])
        

MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_direct_mention(message_text):
    #for some reason starterbot_id outside of this scope returns None type
    starterbot_id = slack_client.api_call("auth.test")["user_id"]

    matches = re.search(MENTION_REGEX, message_text)
    
    # the first group contains the username, the second group contains the remaining message
    
    if matches:
        if not (matches.group(1) == starterbot_id):
            return None
    
        return matches.group(2).strip()


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


#rich man's NLP
#returns tuple(is weather request, city name)
def NLP(sentence):
    sentence = sentence.lower()

    #remove question mark
    if sentence[len(sentence)-1] == '?':
        sentence = sentence[:-1]

    words = sentence.split(' ')

    #check for a combination of any of these
    tests = [['whats','the','weather','like','in'], ['whats','the','weather','in'], ['hows','the','weather','in'], ['whats','the','weather','for'], ['weather','in'], ['weather','for'], ['weather']]

    for test in tests:
        if len(test) >= len(words):
            continue
        total_dist = 0

        #test distance from each word
        for i in range(0, len(test)):
            total_dist += levenshtein(words[i], test[i])


        if total_dist < 3:
            return (True, " ".join(words[len(test):]).title())

    return (False, None)

#actually request the data
#returns string with current conditions
def request(city):
    if not (city in city_dict):
        city = correct(city)
    link = 'http://api.openweathermap.org/data/2.5/weather?id=' + str(city_dict[city]) + '&units=metric&APPID=' + weather_api_key
    response = urllib2.urlopen(link)

    data = json.load(response)
    #return string to print
    return "Current weather in " + city + " is " + data["weather"][0]["description"] + " at " + str(data["main"]["temp"]) + "C"


#process the message
def process_message(msg_echo):
    for update in msg_echo:
        print(update)
        try:
            if 'type' in update and update['type'] == 'message':
                message = parse_direct_mention(update["text"])

                if message is None:
                    continue
                
                (is_req, city_name) = NLP(message)
                #if we're a request, change message to weather
                if is_req:
                    message = request(city_name)

                slack_client.rtm_send_message(update["channel"], message)
        except Exception as e:
            print(str(e))


def main():
    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
    weather_api_key = os.environ.get('API_KEY')
        
    if slack_client.rtm_connect():
        print('RepeaterBot has gone online...')
        while True:
            msg_echo = slack_client.rtm_read()
            process_message(msg_echo)
            time.sleep(1)
    else:
        print("Connection Failed...")

if __name__ == '__main__':
    main()
