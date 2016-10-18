import os
import json

from flask import url_for


class TestMonzoAlexaSkill:

    def test_alive(app, client):
        response = client.get(url_for('home'))
        assert response.status_code == 200
        response_json = response.json
        assert response_json['test'] == "I'm running"

    def test_get_balance(app, monzo, client):
        data = load_json('get_balance.json')
        data['session']['user']['accessToken'] = monzo.access_token
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
        data = load_json('spent_today.json')
        data['session']['user']['accessToken'] = monzo.access_token
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
        data = load_json('last_transaction.json')
        data['session']['user']['accessToken'] = monzo.access_token
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


def load_json(filename):
    filepath = os.path.join(os.path.dirname(__file__), "test_data", filename)
    with open(filepath) as test_file:
        return json.load(test_file)
