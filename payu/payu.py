# -*- coding: utf-8 -*-

import json
import requests
import hashlib

#  PayU Testing data:
MERCHANT_ID = '500238'
ACCOUNT_ID = '500547'
API_LOGIN = '11959c415b33d0c'
API_KEY = '6u39nqhq8ftd0hlvnjfs66eh8c'
PUBLIC_KEY = 'PK186ijn7a2R137B52ZHHm1P9P'
STAGE_PAYMENTS_URL = 'https://stg.api.payulatam.com/payments-api/4.0/service.cgi'
STAGE_REPORTS_URL = 'https://stg.api.payulatam.com/reports-api/4.0/service.cgi'
PAYMENTS_URL = 'https://api.payulatam.com/payments-api/4.0/service.cgi'
REPORTS_URL = 'https://api.payulatam.com/reports-api/4.0/service.cgi'
TOKENIZE_URL = 'http://api.payulatam.com/payments-api/4.0/service'
TEST = True
REPORTS = 'reports'
PAYMENTS = 'payments'


class PayU(object):
    def __init__(self,
                 api_login='',
                 api_key='',
                 account_id='',
                 merchant_id=''):
        """ Datos de la cuenta de PayU necesarios para usar la API"""

        self.api_login = api_login if api_login else API_LOGIN
        self.api_key = api_key if api_key else API_KEY
        self.account_id = account_id if account_id else ACCOUNT_ID
        self.merchant_id = merchant_id if merchant_id else MERCHANT_ID
        self.test = TEST
        self.payments_url = PAYMENTS_URL
        self.reports_url = REPORTS_URL

        if self.test:
            self.payments_url = STAGE_PAYMENTS_URL
            self.reports_url = STAGE_REPORTS_URL

        # Default data for every request
        self.payload = {
            'language': 'es',
            'command': 'PING',
            'merchant': {
                'apiLogin': self.api_login,
                'apiKey': self.api_key
            },
            'test': self.test
        }

        self.order = {
            'language': 'es',
            'accountId': self.account_id
        }

        self.transaction_data = {
            'type': 'AUTHORIZATION_AND_CAPTURE',
            'paymentCountry': 'MX',
        }

        self._currency = 'MXN'

    def _send_request(self, payload, api_type=PAYMENTS):
        headers = {
            'Content-type': 'application/json; charset=utf-8;',
            'Accept': 'application/json;charset=utf-8;'
        }

        payu_url = self.payments_url
        if api_type == REPORTS:
            payu_url = self.reports_url

        response = requests.post(
            payu_url,
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

        response = self._send_request(payload)
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

        response = self._send_request(payload)

        return json.loads(response.text)

    def submit_transaction(self,
                           token_id,
                           reference_code,
                           description,
                           notify_url,
                           value,
                           email,
                           currency=None
                           ):

        order = self.order.copy()

        currency = currency if currency else self._currency
        signature = hashlib.md5('%s~%s~%s~%s~%s' % (
            self.api_key,
            self.merchant_id,
            reference_code,
            value,
            currency
        ))

        order.update({
            'referenceCode': reference_code,
            'description': description,
            'signature': signature.hexdigest(),
            'notifyUrl': notify_url,
            'additionalValues': {
                'TX_VALUE': {
                    'value': value,
                    'currency': 'MXN'
                }
            }
        })

        transaction = self.transaction_data.copy()
        transaction.update({
            'order': order,
            'creditCardTokenId': token_id,
            'payer': {
                'emailAddress': email
            }
        })

        payload = self.payload.copy()

        payload.update({
            'command': 'SUBMIT_TRANSACTION',
            'transaction': transaction
        })

        response = self._send_request(payload)
        return json.loads(response.text)

    def order_detail(self, order_id):
        payload = self.payload.copy()
        payload.update({
            'command': 'ORDER_DETAIL',
            'details': {
                'orderId': order_id
            }
        })

        response = self._send_request(payload, api_type=REPORTS)
        return json.loads(response.text)

