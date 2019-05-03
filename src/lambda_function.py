import datetime
import json
import os
import requests

SLACK_HOOK_URL = "HouseMeetingHook"

def lambda_handler(event, context):
    when = datetime.datetime.strptime(event['time'],'%Y-%m-%dT%H:%M:%SZ')
    if when.day == 6:
        announceUpcommingHouseMeeting(when + datetime.timedelta(days=3))
    elif when.day == 9:
        remindHousemeeting(when)

def announceUpcommingHouseMeeting(hmDateTime):
    weekDayName = hmDateTime.strftime("%A")
    hmTime = "19:00h"
    if weekDayName == "Saturday" or weekDayName == "Sunday":
        hmTime = "14:00h"
    
    hookWithSlackBot({
        "text": """Dear <!channel>

We will have the house meeting this Saturday the {} at {}

Feel free to add topics and proposals you'd like to discuss in the common agenda here:
https://docs.google.com/document/d/1rtIzrTK3MugLD7A1r7w5Xmu8ebzJNPH-Vi6cGEsP6fY/edit#

Love :heart:""".format(hmDateTime.strftime("%A the %dth of %B"), hmTime)})

def remindHousemeeting(hmDateTime):
    if scheduleForDayIsCorrect(hmDateTime):
        hookWithSlackBot({"text": "House Meeting starts now! <!channel> :unicorn_face::cherry_blossom::heart:"})

def scheduleForDayIsCorrect(hmDateTime):
    weekDayName = hmDateTime.strftime("%A")
    isWeekend = weekDayName == "Saturday" or weekDayName == "Sunday"
    return (isWeekend and hmDateTime.hour == 14) or (not isWeekend and hmDateTime.hour == 19)

def hookWithSlackBot(message):
    r = requests.post(os.environ[SLACK_HOOK_URL], json=message)