#!/usr/bin/env python


import json
import requests

def get_weather(city):

  url2 = "select item.condition from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "') and u='c'"
  url = "https://query.yahooapis.com/v1/public/yql?q=" + url2 + "&format=json"
  r = requests.get(url)
  if r.status_code == requests.codes.ok:
    dic = json.loads(r.text)

    temp = dic['query']['results']['channel']['item']['condition']['temp']
    desc = dic['query']['results']['channel']['item']['condition']['text']
    print '#'*40 + '\n'
    print 'Weather in {} is {} Celsius, {}'.format(city, temp, desc)
    print '\n' + '#'*40 
  else:
    print("Can't get URL")
    exit()

if __name__ == '__main__':
  city = "Seattle"
  get_weather(city)
