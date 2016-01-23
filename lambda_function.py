from __future__ import print_function
import httplib
import json
import re
import urllib


def lambda_handler(event, context):
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    return get_welcome_response()


def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "Ask":
        return ask_for_property(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])


# --------------- Functions that control the skill's behavior ------------------

#this whole thing is a placeholder for the moment, it's not a real interaction
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the I. M. D. B. skill."
    reprompt_text = "Please ask me a movie question."
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def ask_for_property(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True

    if 'Movie' in intent['slots'] and 'Property' in intent['slots']:
        movie_input = intent['slots']['Movie']['value']
        property = intent['slots']['Property']['value']
        values = get_imdb_properties(movie_input)
        movie = values["Title"]

        if property == 'rating' or property == 'score':
            rating = values["imdbVotes"].replace(",", "")
            length = len(str(rating))
            rough = str(round(float(rating), 3-length)).replace(".0", "")
            speech_output = "The " + property + " of " + movie + " is " + values["imdbRating"] + " with about " + rough + " votes."
        else:
            value = get_imdb_property(movie, property)
            speech_output = "The " + property + " of " + movie + " is " + value
        
        reprompt_text = ""
    else:
        speech_output = "I could not understand the question.  Are you some sort of idiot?"
        reprompt_text = "Well obviously you're an idiot then."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_imdb_property(movie, property):
    document = get_imdb_properties(movie)
    imdb_property = translate_property(property)
    value = document[imdb_property]

    return value

def get_imdb_properties(movie):
    site = "www.omdbapi.com"
    imdb_id = get_imdb_id(movie)
    resource = "/?i=" + urllib.quote_plus(imdb_id)
    document = http_get_json(site, resource)

    return document


def translate_property(property):
    return {
        "year": "Year",
        "genre": "Genre",
        "director": "Director",
        "plot": "Plot",
        "rating": "imdbRating",
        "score": "imdbRating"
    }[property]


def get_imdb_id(movie):
    site = "ajax.googleapis.com"
    resource = "/ajax/services/search/web?v=1.0&q=imdb+" + urllib.quote_plus(movie)
    document = http_get_json(site, resource)

    link = document["responseData"]["results"][0]["url"]
    pattern = re.compile("http://www\.imdb\.com/title/(tt\d+)/")
    match = pattern.match(link)
    imdb_id = match.group(1)

    return imdb_id


def http_get_json(site, resource):
    response = http_get(site, resource)
    document = json.loads(response)

    return document


def http_get(site, resource):
    print("HTTP GET: " + site + resource)

    connection = httplib.HTTPSConnection(site)
    connection.request("GET", resource)
    response = connection.getresponse()
    print(response.status, response.reason)

    data = response.read()
    print(data)

    connection.close()

    return data

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }