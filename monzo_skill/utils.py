# -*- coding: utf-8 -*-

from datetime import datetime

from dateutil import parser

from monzo import MonzoClient


def get_balance(access_token):
    monzo = MonzoClient(access_token=access_token)
    monzo.update_tokens()
    balance = monzo.get_balance()
    return money_to_string(balance['balance'], balance['currency'])


def get_spent_today(access_token):
    monzo = MonzoClient(access_token=access_token)
    monzo.update_tokens()
    balance = monzo.get_balance()
    return money_to_string(balance['spend_today'], balance['currency'])


def get_last_transaction(access_token):
    monzo = MonzoClient(access_token=access_token)
    monzo.update_tokens()
    # Should limit transactions to the last month
    transaction = monzo.list_transactions(limit=100000)[::-1][0]

    amount = money_to_string(transaction['amount'], transaction['currency'])
    when = date_to_speech(transaction['created'])
    merchant = transaction['merchant']['name']
    return {
        'amount': amount,
        'when': when,
        'merchant': merchant,
    }


def date_to_speech(date_string):
    compare_time = parser.parse(date_string).replace(tzinfo=None)
    days_ago = (datetime.today() - compare_time).days
    if days_ago == 0:
        return 'today'
    if days_ago == 1:
        return 'yesterday'
    if days_ago == 7:
        return '1 week ago'
    if days_ago > 31:
        return 'over a month ago'
    return '{0} days ago'.format(days_ago)


def money_to_string(int_money, currency):
    if int_money < 0:
        int_money = int_money * -1
    decimal_money = format(float(int_money) / float(100), '.2f')
    currency_symbol_mapping = {
        'GBP': u'£',
        'USD': u'$',
        'EUR': u'€',
    }
    currency_symbol = currency_symbol_mapping[currency]
    return u'{0}{1}'.format(currency_symbol, decimal_money)


def build_speech_response(title, output, reprompt_text, should_end_session):
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
