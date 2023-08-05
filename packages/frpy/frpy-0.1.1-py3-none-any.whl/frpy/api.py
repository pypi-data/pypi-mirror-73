import json
import requests

__all__ = ['getHome', 'getCategory', 'getLead', 'getUser', 'getTrack', 'getRandom']

def getFeaturedGhosts():
    response = requests.get("https://raw.githubusercontent.com/Calculus0972/Official_Featured_Ghosts/master/ghosts.json")
    return response.json()

def getHome():
    response = requests.get("https://www.freeriderhd.com?ajax=true")
    return response.json()

def getLead():
    response = requests.get("https://www.freeriderhd.com/leaderboards/player/lifetime?ajax=true")
    return response.json()

def getCategory(category):
    response = requests.get("https://www.freeriderhd.com/{}?ajax".format(category))
    return response.json()

def getUser(username):
    response = requests.get("https://www.freeriderhd.com/u/{}?ajax=true".format(username))
    return response.json()

def getTrack(track_id):
    response = requests.get("https://www.freeriderhd.com/t/{}?ajax=true".format(track_id))
    return response.json()

def getRandom():
    response = requests.get("https://www.freeriderhd.com/random/track?ajax=true")
    return response.json()