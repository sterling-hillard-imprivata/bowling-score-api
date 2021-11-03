# Bowling Score API

---

## Table of Contents
- Overview
- Set up
- Running the Api
- Testing

---

## Overview
This API uses the Django Rest Framework feature to replicate a Bowling scoring application. This project was inspired by the Software Engineering and Hiring teams at Zebra. 

Project Specs:
"The challenge is to implement a bowling scoring REST API (and optional front end). Basically, something that takes in pins knocked down for players and keeps track of them and calculates and provides their scores.
"
Used this as reference: 
http://bowling.about.com/od/rulesofthegame/a/bowlingscoring.htm


- If you were in a bowling alley and looked at the display, it would be the service that powered the numbers behind the display.
- Use production-quality code that's well-tested and well-documented. 
- Show usage of a REST framework
- Any modern language is permissable so I will use Python. 
- The solution should score as the game progresses rather than just at the end.

## Set up
This project requires prior installations of both Python and Django. 

- If you do not have either, you may follow the links below:
Python 3x: https://www.python.org/downloads/
Django:https://docs.djangoproject.com/en/3.2/topics/install/


- Clone the repository to your desired directory folder and enter the repo
```bash

mkdir <folder-name>
cd <folder-name>

git clone git@github.com:sterlingdhill/bowling-score-api.git

cd bowling-score-api/bowlingscore

```

### Wiping your data and starting fresh
There are some records in the API already within the sqlite file. If you would like to start fresh, simply type in the 
command python manage.py flush. You will be prompted if you would like to erase the dataset, input Yes

## Running the AP
Enter the project 'bowlingscore' and run the command > python manage.py runserver

```bash
cd bowlingscore

python manage.py runserver
```

- From here we are given the server location: 127.0.0.1:8000/. We want to go straight to the api serializer so input **127.0.0.1:8000/api** into the browser.

![Bowling Score API directory](bowlingscore/documentation/snap_1.JPG "Directory")

From here we will choose the 'players' endpoint so click that link to begin creating a player.

### Creating, Retrieving, Updating and Deleting Players

![Players database](bowlingscore/documentation/snap_2.JPG "Create a Player")

You can enter the players name and which game number they are to be apart of, both of these fields are required so the database and API can identify which players go with which game. 

Note: You **CANNOT** have a duplicate name for the same game. 

If you would like to update or delete characters you will need to input their id number in the url endpoint. For example:
**127.0.0.1:8000/api/players/1**

![Players database](bowlingscore/documentation/snap_3.JPG "Updating or Deleting a Player")


## Testing
