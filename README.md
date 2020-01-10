# Escape the Room by xenus
## Roster and Role:
- Biraj Chowdury (Python)
- Nahi Khan (HTML and CSS)
- Henry Liu (Project Manager)
- Albert Wan (Database and HTML)

## Project Overview
The overall goal of the project is to create a game with a storyline where players attempt to escape the universe Xenus. We will have puzzles like type racer, Galactica, trivia, chance, blackjack, snake and computation problems which will be timed and will only be available once the player completes the puzzles before that one. Through the use of REST APIs, JavaScript, Flask, and databases managed by SQLite, our site will give players a fun game that they won't want to stop playing.

## APIs Utilized:
[Diceful API](http://roll.diceapi.com/)
  - We will use this API to roll die for our chance game.

[Deck Of Cards](https://deckofcardsapi.com/)
  - We will use this API to get cards for our blackjack game.

[NBA Player API](https://nba-players.herokuapp.com)
  - we will use this API to get pictures for users' profile pictures.

[The Open Trivia API](https://opentdb.com/api_config.php)
  - We will use this API to get trivia questions for use in our trivia game.


## How to Run the Project:  
### Requirements:
Python3 and pip is required to run the project  
[Download Python3 here](https://www.python.org/downloads/) (pip3 comes with python3 download)

### Creating and activating a virtual environment:
`$ python3 -m venv <name>`  
`$ ./<name>/bin/activate`

### Clone the project and install requirments.txt:
`$ git clone git@github.com:hliu01/xenus.git`  
After activating the virutal environment:  
`(venv)$ cd xenus`    
`(venv)$ pip3 install -r doc/requirements.txt`  

### Run the project: 
`$ python3 app.py`  

View the webpage by opening a web browser and visiting: http://127.0.0.1:5000/

---
© Copyright 2020 xenus -- - Biraj Chowdury, Nahi Khan, Henry Liu & Albert Wan
