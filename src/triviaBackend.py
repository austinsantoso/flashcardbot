import json
import requests

API_URL = "https://opentdb.com/api.php?amount=1&category=15&type=boolean"

def get_trivia():
    """Fetch joke from the web and return."""
    url = API_URL
    headers = {'Accept': 'application/json'}
    triviaJson = requests.get(url, headers=headers).json().get('results')[0]
    triviaQuestion = triviaJson.get('question')
    triviaAnswer = triviaJson.get('correct_answer')
    return (triviaQuestion, triviaAnswer)
