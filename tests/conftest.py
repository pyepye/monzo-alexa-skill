import os
import sys
import json
import subprocess
import webbrowser
from datetime import datetime
from urlparse import urlparse, parse_qs

import pytest

from monzo import MonzoClient

from monzo_skill.app import app as mas_app


@pytest.fixture
def app():
    app = mas_app
    return app


@pytest.fixture(scope="module")
def monzo():
    client_secret = os.getenv('MONZO_CLIENT_SECRET')
    if not client_secret:
        raise ValueError('MONZO_CLIENT_SECRET environment variable must be set')  # NOQA
    client_id = os.getenv('MONZO_CLIENT_ID')
    if not client_id:
        raise ValueError('MONZO_CLIENT_ID environment variable must be set')

    try:
        base_url = os.path.dirname(__file__)
        token_file = os.path.join(base_url, 'token_info.json')
        with open(token_file) as data_file:
            tokens = json.load(data_file)
    except IOError:
        tokens = setup_access(client_id, client_secret)

    expires_at = datetime.strptime(tokens['expires_at'], "%Y-%m-%dT%H:%M:%S.%f")  # NOQA
    if datetime.now() > expires_at:
        tokens = setup_access(client_id, client_secret)

    monzo = MonzoClient(access_token=tokens['access_token'])
    return monzo


def setup_access(client_id, client_secret):

    monzo = MonzoClient(client_id, client_secret, 'http://example.com/login/')
    auth_url = monzo.get_authorization_code()

    # pdb is needed to allow for the raw_input to stop the test.
    # Just type 'c' to continue on the breakpoint
    import pdb
    pdb.set_trace()

    print '\nA browser will now open, please login and copy the URL once authenticated'  # NOQA
    if sys.platform == 'darwin':
        subprocess.Popen(['open', auth_url])
    else:
        webbrowser.open_new_tab(auth_url)

    url = raw_input("\nPlease enter the url from the 'Log in to Monzo' button in the authentication email: ")  # NOQA
    url = urlparse(url)
    import pytest
    pytest.set_trace()
    query = parse_qs(url.query)
    code = query['code'][0]
    token_info = monzo.get_access_token(code)

    base_dir = os.path.dirname(__file__)
    token_file = '{0}/token_info.json'.format(base_dir)
    with open(token_file, 'w') as fp:
        json.dump(token_info, fp)

    print 'Token info exported to: {0}'.format(token_file)
    return token_info
