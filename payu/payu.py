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
    TRANSACTION_RESPONSE_CODES = {
        'ERROR': 'Ocurrió un error general.',
        'APPROVED': 'La transacción fue aprobada.',
        'ANTIFRAUD_REJECTED': 'La transacción fue rechazada por el sistema anti-fraude.',
        'PAYMENT_NETWORK_REJECTED': 'La red financiera rechazó la transacción.',
        'ENTITY_DECLINED': 'La transacción fue declinada por el banco o por la red financiera debido a un error.',
        'INTERNAL_PAYMENT_PROVIDER_ERROR': 'Ocurrió un error en el sistema intentando procesar el pago.',
        'INACTIVE_PAYMENT_PROVIDER': 'El proveedor de pagos no se encontraba activo.',
        'DIGITAL_CERTIFICATE_NOT_FOUND': 'La red financiera reportó un error en la autenticación.',
        'INVALID_EXPIRATION_DATE_OR_SECURITY_CODE': 'El código de seguridad o la fecha de expiración estaba inválido.',
        'INSUFFICIENT_FUNDS': 'La cuenta no tenía fondos suficientes.',
        'CREDIT_CARD_NOT_AUTHORIZED_FOR_INTERNET_TRANSACTIONS': 'La tarjeta de crédito no estaba autorizada para transacciones por Internet.',
        'INVALID_TRANSACTION': 'La red financiera reportó que la transacción fue inválida.',
        'INVALID_CARD': 'La tarjeta es inválida.',
        'EXPIRED_CARD': 'La tarjeta ya expiró.',
        'RESTRICTED_CARD': 'La tarjeta presenta una restricción.',
        'CONTACT_THE_ENTITY': 'Debe contactar al banco.',
        'REPEAT_TRANSACTION': 'Se debe repetir la transacción.',
        'ENTITY_MESSAGING_ERROR': 'La red financiera reportó un error de comunicaciones con el banco.',
        'BANK_UNREACHABLE': 'El banco no se encontraba disponible.',
        'EXCEEDED_AMOUNT': 'La transacción excede un monto establecido por el banco.',
        'NOT_ACCEPTED_TRANSACTION': 'La transacción no fue aceptada por el banco por algún motivo.',
        'ERROR_CONVERTING_TRANSACTION_AMOUNTS': 'Ocurrió un error convirtiendo los montos a la moneda de pago.',
        'EXPIRED_TRANSACTION': 'La transacción expiró.',
        'PENDING_TRANSACTION_REVIEW': 'La transacción fue detenida y debe ser revisada, esto puede ocurrir por filtros de seguridad.',
        'PENDING_TRANSACTION_CONFIRMATION': 'La transacción está pendiente de ser confirmada.',
        'PENDING_TRANSACTION_TRANSMISSION': 'La transacción está pendiente para ser trasmitida a la red financiera. Normalmente esto aplica para transacciones con medios de pago en efectivo.',
        'PAYMENT_NETWORK_BAD_RESPONSE': 'El mensaje retornado por la red financiera es inconsistente.',
        'PAYMENT_NETWORK_NO_CONNECTION': 'No se pudo realizar la conexión con la red financiera.',
        'PAYMENT_NETWORK_NO_RESPONSE': 'La red financiera no respondió.',
        'FIX_NOT_REQUIRED': 'Clínica de transacciones: Código de manejo interno.'
    }

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

