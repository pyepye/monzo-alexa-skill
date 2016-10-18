import os
import json

from flask import url_for

from monzo_skill import settings


class TestMonzoAlexaSkill:

    def test_alive(app, client):
        response = client.get(url_for('home'))
        assert response.status_code == 200
        response_json = response.json
        assert response_json['test'] == "I'm running"

    def test_get_balance(app, monzo, client):
        data = load_test_data('get_balance.json', monzo)
        response = client.post(
            url_for('alexa'),
            headers={'content-type': 'application/json'},
            data=json.dumps(data)
        )
        assert response.status_code == 200
        response = response.json
        assert response.keys() == ['version', 'response', 'sessionAttributes']
        assert response['response'].keys() == ['outputSpeech', 'shouldEndSession', 'reprompt', 'card']  # NOQA
        assert response['response']['outputSpeech']['text'].startswith('Your Monzo balance is ')  # NOQA
        assert response['response']['card']['content'].startswith('Your Monzo balance is ')  # NOQA
        assert response['response']['card']['title'] == 'Monzo: Your balance'

    def test_spent_today(app, monzo, client):
        data = load_test_data('spent_today.json', monzo)
        response = client.post(
            url_for('alexa'),
            headers={'content-type': 'application/json'},
            data=json.dumps(data)
        )
        assert response.status_code == 200
        response = response.json
        assert response.keys() == ['version', 'response', 'sessionAttributes']
        assert response['response'].keys() == ['outputSpeech', 'shouldEndSession', 'reprompt', 'card']  # NOQA
        assert response['response']['outputSpeech']['text'].startswith('Your have spent ')  # NOQA
        assert response['response']['card']['content'].startswith('Your have spent ')  # NOQA
        assert response['response']['card']['title'] == 'Monzo: Spent today'

    def test_last_transaction(app, monzo, client):
        data = load_test_data('last_transaction.json', monzo)
        response = client.post(
            url_for('alexa'),
            headers={'content-type': 'application/json'},
            data=json.dumps(data)
        )
        assert response.status_code == 200
        response = response.json
        assert response.keys() == ['version', 'response', 'sessionAttributes']
        assert response['response'].keys() == ['outputSpeech', 'shouldEndSession', 'reprompt', 'card']  # NOQA
        assert response['response']['outputSpeech']['text'].startswith('Your last transaction was for')  # NOQA
        assert response['response']['card']['content'].startswith('Your last transaction was for')  # NOQA
        assert response['response']['card']['title'] == 'Monzo: Your last transaction'  # NOQA


def load_test_data(filename, monzo):
    filepath = os.path.join(os.path.dirname(__file__), "test_data", filename)
    with open(filepath) as test_file:
        data = json.load(test_file)
    data['session']['user']['accessToken'] = monzo.access_token
    data['session']['application']['applicationId'] = settings.ALEXA_APP_ID
    return data
