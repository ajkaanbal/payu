# -*- coding: utf-8 -*-

import json
import requests

PAYU_MERCHANT_ID = '500238'
PAYU_ACCOUNT_ID = '1'
PAYU_API_LOGIN = '11959c415b33d0c'
PAYU_API_KEY = '6u39nqhq8ftd0hlvnjfs66eh8c'
PAYU_PUBLIC_KEY = 'PK186ijn7a2R137B52ZHHm1P9P'
PAYU_PAYMENTS_URL = 'https://stg.api.payulatam.com/payments-api/4.0/service.cgi'
PAYU_REPORTS_URL = 'https://stg.api.payulatam.com/reports-api/4.0/service.cgi'
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
        self.payload = {
            'language': 'es',
            'command': 'GET_TOKENS',
            'merchant': {
                'apiLogin': self.api_login,
                'apiKey': self.api_key
            }
        }

    def send_request(self, payload):
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.post(
            self.payments_url,
            data=json.dumps(payload),
            headers=headers,
            verify=False
        )
        print 'REQUEST: %s' % payload
        print 'RESPONSE: %s' % json.dumps(response.text, indent=2)
        return response

    def create_token(self,
                     payer_id,
                     full_name,
                     payment_method,
                     card_number,
                     expiration_date):

        payload = self.payload.copy()

        payload.update({
            'command': 'CREATE_TOKEN',
            'creditCardToken': {
                'payerId': payer_id,
                'name': full_name,
                'paymentMethod': payment_method,
                'number': card_number,
                'expirationDate': expiration_date
            }
        })

        response = self.send_request(payload)
        return json.loads(response.text)


    def get_tokens(self, payer_id, token_id):
        """ Información sobre el token """

        payload = self.payload.copy()

        payload.update({
            'command': 'GET_TOKENS',
            'creditCardTokenInformation': {
                'payerId': payer_id,
                'creditCardTokenId': token_id,
                "startDate": "2014-01-15T15:30:00",
                "endDate": "2015-01-16T17:40:00"
            }
        })

        response = self.send_request(payload)

        return json.loads(response.text)


