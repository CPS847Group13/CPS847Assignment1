import json
import io
import sys
import urllib.request
import re

#API_KEY = '';

#list is used for fixing typos
city_list = [ ]
#dict is used to store ID once we found the city
city_dict = { }



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
    
def correct(word):
    min_dist = sys.maxsize
    closest_word = None
    for city in city_list:
        dist = levenshtein(city, word)
        if dist < min_dist:
            min_dist = dist
            closest_word = city

    return closest_word
    
    
def request(city):
    if not (city in city_dict):
        city = correct(city)

    with urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?id=' + str(city_dict[city]) + '&units=metric&appid=' + API_KEY) as url:
        data = json.loads(url.read().decode())
        print("Current weather in " + city + " is " + data["weather"][0]["description"] + " at " + str(data["main"]["temp"]) + "C")
    
#return if true and where to split the string
def is_weather_request(sentence):
    sentence = sentence.lower()

    if levenshtein("whats the weather in", sentence) < 16:
        return (True,4)
    
    if levenshtein("whats weather in", sentence) < 16 or levenshtein("whats weather for", sentence) < 16:
        return (True, 3)
    
    if levenshtein("weather in", sentence) < 16 or levenshtein("weather for", sentence) < 16:
        return (True,2)
    
    if levenshtein("weather", sentence) < 16:
        return (True,1)

    return (False,0)
    
#split sentence and get remaining
def get_location(sentence, split_loc):

    #remove question mark
    if sentence[len(sentence)-1] == '?':
        sentence = sentence[:-1]

    #split string
    split = sentence.split(' ')[split_loc:]

    return " ".join(split)
    
    
if __name__ == '__main__':
    ##read in city list
    #with open('city.list.json', mode="r", encoding="utf-8") as f:
    #    json_cities = json.load(f)
    
    ##create a dictionary of cities for id, and a list for corrections
    #for city in json_cities:
    #    city_dict[city["name"]] = city["id"]
    #    city_list.append(city["name"])
    
    #request("New Yrk")
    
    (is_weather, split) = is_weather_request("Weather in New York City?")
    
    print(get_location("Weather in New York City?", split))
    #is_weather_request("Weather in New York City")
    #is_weather_request("Weather fr New York City")
    #is_weather_request("what's weather in New York City")
    
    