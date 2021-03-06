# Monza Alexa Skill API

Custom alexa skill API for [Monzo](https://monzo.com/) with help using the my [monzo-python](https://github.com/pyepye/monzo-python) api wrapper.

A basic and slow example of the API working with echosim.io:
https://www.youtube.com/watch?v=Llodh4puJMo

## Testing
* Create a new Monzo OAuth Client for testing
* `export MONZO_CLIENT_ID=#####`
* `export MONZO_CLIENT_SECRET=#####`
* `py.test tests -v`


## Setup

__*WARNING*__

Setting up and testing this custom skill is not very friendly. This is because you need to setup your own Monzo OAuth client, you need a server to run the API and you will also need to setup your own custom Alexa skill (as each none published custom skill is linked to a developer account).

### Prerequisites

* A HTTPS server with python installed to run the flask code
* A Monzo developer account and a OAuth Client (https://developers.monzo.com/)
* A Amazon developer account (https://developer.amazon.com)

### Server Setup

This is a basic and poor explanation on the setup, I actually use supervisor and nginx to run the flask app (see `server_setup/`). If you want help with setting up a server let me know.

1. Fork this repo
2. `git clone [yourfork] && cd monzo-alexa-skill`
3. `pip install -r requirements.txt`
4. `pip install -e git+git@[yourfork]#egg=Package` # Replace the github link with your fork
5. `export ALEXA_APP_ID=#####`  # You will need to have done the Alexa Setup for this
6. `PYTHONPATH=./ python monzo_skill/app.py`
7. Test it's running at https://[yourserver]/


### Alexa Setup

_Note: If you are using [echosim.io](http://echosim.io) make sure you skill language is `English (U.S.)` or you skill will not be recognised_

1. Add a new Alexa skill at https://developer.amazon.com/edw/home.html#/skills/list
2. Skill Information
    * Skill Type: Custom Interaction Model
    * Name: Monzo
    * Invocation Name: Monzo
    * Audio Player: No
3. Interaction Model
    * Intent Schema: Copy from `monzo_skill/intent_shema.json`
    * Sample Utterances: Copy from `monzo_skill/utterances.txt`
4. Configuration
    * Service Endpoint Type: HTTPS
    * HTTPS URL: Europe - https://[yourserver]/alexa/
    * Account Linking: Yes
    * Authorization URL: https://auth.getmondo.co.uk/
    * Client Id: From your Monzo OAuth Client
    * Redirect URL: Take the redirect URL and put it into your Monzo OAuth Client
    * Authorization Grant Type: Auth Code Grant
    * Access Token URI: https://api.monzo.com/oauth2/token
    * Client Secret: From your Monzo OAuth Client
    * Client Authentication Scheme: HTTP Basic
5. SSL Certificate
    * Certificate for EU Endpoint:  My development endpoint has a certificate
6. Login to [echosim.io](http://echosim.io)
7. Login to http://alexa.amazon.com/
8. Go to Skills > Your Skills (top right) > Monzo > Link Account
9. You are ready to go. Get testing on echosim.io


## ToDo:
* Add logging
