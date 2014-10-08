# -*- coding: utf-8 -*-

import json
import requests

PAYU_MERCHANT_ID = '500238'
PAYU_ACCOUNT_ID = '1'
PAYU_API_LOGIN = '11959c415b33d0c'
PAYU_API_KEY = '6u39nqhq8ftd0hlvnjfs66eh8c'
PAYU_PUBLIC_KEY = 'PK186ijn7a2R137B52ZHHm1P9P'
PAYU_PAYMENTS_URL = 'https://stg.api.payulatam.com/payments-api/4.0/service'
PAYU_REPORTS_URL = 'https://stg.api.payulatam.com/reports-api/4.0/service'
PAYU_TOKENIZE_URL = 'http://api.payulatam.com/payments-api/4.0/service'
PAYU_TEST = True


class PayU(object):
    def __init__(self):
        """ Datos de la cuenta de PayU necesarios para usar la API"""

        self.api_login = PAYU_API_LOGIN
        self.api_key = PAYU_API_KEY
        self.payments_url = PAYU_PAYMENTS_URL
        self.reports_url = PAYU_REPORTS_URL
        self.test = PAYU_TEST

    def token_info(self, token):
        """ Información sobre el token """

        payload = {
            'language': 'es',
            'command': 'GET_TOKENS',
            'merchant': {
                'apiLogin': self.api_login,
                'apiKey': self.api_key
            },
            'creditCardTokenInformation': {
                'payerId': token.user.id,
                'creditCardTokenId': token.token,
                'startDate': '2010-01-01T12:00:00',
                'endDate': '2015-01-01T12:00:00'
            }
        }
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }

        r = requests.post(
            self.payments_url,
            data=json.dumps(payload),
            headers=headers,
            verify=False
        )

        print('Value of r is {}'.format(r))
        print (r.text)

