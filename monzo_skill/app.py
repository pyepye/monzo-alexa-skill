from flask import Flask, request, jsonify

# from monzo import MonzoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeme'


@app.route('/')
def home():
    return jsonify(test="I'm running")


@app.route('/alexa/', methods=['POST'])
def alexa():
    event = request.get_json()
    if (event['session']['application']['applicationId'] !=
            'amzn1.ask.skill.98d21241-9161-42af-a29b-5cf778c12357'):
        raise ValueError('Invalid Application ID')

    # If not acccess code
        # Reply with session request - build_linked_account(session_attributes)

    if event['session']['new']:
        on_session_started(
            {'requestId': event['request']['requestId']}, event['session']
        )

    if event['request']['type'] == 'LaunchRequest':
        response = on_launch(event['request'], event['session'])
    elif event['request']['type'] == 'IntentRequest':
        response = on_intent(event['request'], event['session'])
    elif event['request']['type'] == 'SessionEndedRequest':
        response = on_session_ended(event['request'], event['session'])
    return jsonify(**response)


def on_session_started(session_started_request, session):
    print 'Starting new session.'


def on_launch(launch_request, session):
    return get_welcome_response()


def on_intent(intent_request, session):
    # intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == 'GetBalance':
        return get_balance()
    elif intent_name == 'LastTransaction':
        return get_last_transaction()
    elif intent_name == 'AMAZON.HelpIntent':
        return get_welcome_response()
    elif (intent_name == 'AMAZON.CancelIntent' or
          intent_name == 'AMAZON.StopIntent'):
        return handle_session_end_request()
    else:
        raise ValueError('Invalid intent')


def on_session_ended(session_ended_request, session):
    print 'Ending session.'
    # Cleanup goes here...


def handle_session_end_request():
    card_title = 'Monzo: Thanks'
    speech_output = u'Thank you for using the Monzo Alexa skill.'
    should_end_session = True
    response = build_speechlet_response(
        card_title, speech_output, None, should_end_session
    )
    return build_response({}, response)


def get_welcome_response():
    session_attributes = {}
    card_title = 'Monzo'
    speech_output = """Welcome to the Alexa Monzo skill. Ask for you balance or
                    information on your last transaction."""
    reprompt_text = """Please ask me for your balance or transaction history."""  # NOQA
    should_end_session = False

    reponse = build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session
    )
    return build_response(session_attributes, reponse)


def get_balance():
    session_attributes = {}
    card_title = 'Your Monzo balance'
    reprompt_text = ''
    should_end_session = False

    balance = 100

    speech = unicode('Your Monzo balance is £{0}.'.format(balance), 'utf-8')
    response = build_speechlet_response(
        card_title, speech, reprompt_text, should_end_session
    )
    return build_response(session_attributes, response)


def get_last_transaction():
    session_attributes = {}
    card_title = 'Monzo: Last transaction'
    reprompt_text = ''
    should_end_session = False

    amount = 100

    speech_output = u'Your last transaction was for £{0}'.format(amount)
    response = build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session
    )
    return build_response(session_attributes, response)


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
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


def build_linked_account(session_attributes):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": """
                    You must have a Monzo account to use this skill.
                    Please use the Alexa app to link your Amazon account with
                     your Monzo Account."""
            },
            "card": {
                "type": "LinkAccount"
            },
            "shouldEndSession": False
        }
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8006)
