# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify

from monzo_skill.utils import (
    get_balance, get_spent_today, get_last_transaction,
    build_speech_response, build_linked_account, build_response
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeme'


@app.route('/')
def home():
    return jsonify(test="I'm running")


@app.route('/alexa/', methods=['POST'])
def alexa():
    event = request.get_json()
    app_id = event['session']['application']['applicationId']
    if app_id != 'amzn1.ask.skill.98d21241-9161-42af-a29b-5cf778c12357':
        raise ValueError('Invalid Application ID')

    try:
        access_token = event['session']['user']['accessToken']
    except KeyError:
        jsonify(build_linked_account({}))

    if event['session']['new']:
        on_session_started(
            {'requestId': event['request']['requestId']}, event['session']
        )

    request_type = event['request']['type']
    if request_type == 'LaunchRequest':
        response = on_launch(event['request'], event['session'])
    elif request_type == 'IntentRequest':
        response = on_intent(event['request'], event['session'], access_token)
    elif request_type == 'SessionEndedRequest':
        response = on_session_ended(event['request'], event['session'])
    return jsonify(**response)


def on_session_started(session_started_request, session):
    print 'Starting new session.'


def on_launch(launch_request, session):
    return welcome_response()


def on_intent(intent_request, session, access_token):
    # intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == 'GetBalance':
        return balance(access_token)
    elif intent_name == 'SpentToday':
        return spent_today(access_token)
    elif intent_name == 'LastTransaction':
        return last_transaction(access_token)
    elif intent_name == 'AMAZON.HelpIntent':
        return welcome_response()
    elif intent_name in ['AMAZON.CancelIntent', 'AMAZON.StopIntent']:
        return handle_session_end_request()
    else:
        raise ValueError('Invalid intent')


def on_session_ended(session_ended_request, session):
    print 'Ending session.'
    # Cleanup goes here...


def handle_session_end_request():
    card_title = 'Monzo: Thank you'
    speech_output = u'Thank you for using the Monzo Alexa skill.'
    should_end_session = True
    response = build_speech_response(
        card_title, speech_output, None, should_end_session
    )
    return build_response({}, response)


def welcome_response():
    session_attributes = {}
    card_title = 'Monzo: Welcome'
    speech_output = """Welcome to the Alexa Monzo skill. Ask for you balance or
                    information on your last transaction."""
    reprompt_text = """Please ask me for your balance or transaction history."""  # NOQA
    should_end_session = False

    reponse = build_speech_response(
        card_title, speech_output, reprompt_text, should_end_session
    )
    return build_response(session_attributes, reponse)


def balance(access_token):
    session_attributes = {}
    card_title = 'Monzo: Your balance'
    reprompt_text = ''
    should_end_session = False

    balance = get_balance(access_token)
    speech = u'Your Monzo balance is {0}.'.format(balance)
    response = build_speech_response(
        card_title, speech, reprompt_text, should_end_session
    )
    return build_response(session_attributes, response)


def spent_today(access_token):
    session_attributes = {}
    card_title = 'Monzo: Spent today'
    reprompt_text = ''
    should_end_session = False

    spent_today = get_spent_today(access_token)
    speech = u'Your have spent {0} today.'.format(spent_today)
    response = build_speech_response(
        card_title, speech, reprompt_text, should_end_session
    )
    return build_response(session_attributes, response)


def last_transaction(access_token):
    session_attributes = {}
    card_title = 'Monzo: Your last transaction'
    reprompt_text = ''
    should_end_session = False

    last_transaction = get_last_transaction(access_token)
    amount = last_transaction['amount']
    when = last_transaction['when']
    merchant = last_transaction['merchant']
    speech_output = u'Your last transaction was for {0} {1} at {2}'.format(
        amount, when, merchant
    )

    response = build_speech_response(
        card_title, speech_output, reprompt_text, should_end_session
    )
    return build_response(session_attributes, response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8006)
