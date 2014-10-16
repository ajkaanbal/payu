import re
import unittest


class PayUTest(unittest.TestCase):

    def setUp(self):
        from payu import PayU
        self.payu = PayU()

    def test_create_token(self):
        response = self.payu.create_token(
            '10',
            'Juan Perez',
            'VISA',
            '4111111111111111',
            '2014/12'
        )
        self.assertTrue(response.get('code'))
        self.assertEqual(response.get('code'), 'SUCCESS')

    def test_get_tokens(self):
        response = self.payu.get_tokens(
            '10',
            'a6ab07a8-2bc6-4c39-9ad1-cc18d6d53bf8'
        )
        self.assertTrue(response.get('code'))
        self.assertEqual(response.get('code'), 'SUCCESS')

    def test_submit_transaction(self):
        device_id = 'vghs6tvkcle931686k1900o6e1'
        ip_address = '127.0.0.1'
        cookie = 'pt1t38347bs6jc9ruv2ecpv7o2'
        user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:18.0) Gecko/20100101 Firefox/18.0'

        payer =  {
            'merchantPayerId': '1',
            'fullName': 'First name and second payer name',
            'emailAddress': 'payer_test@test.com',
            'contactPhone': '7563126',
            'dniNumber':'5415668464654',
            'billingAddress': {
                'street1': 'Calle Zaragoza esquina',
                'street2': 'calle 5 de Mayo',
                'city': 'Monterrey',
                'state': 'Nuevo Leon',
                'country': 'MX',
                'postalCode': '64000',
                'phone': '7563126'
            }
        }
        buyer = payer.copy()
        buyer.update({
            'merchantBuyerId': buyer.pop('merchantPayerId'),
            'shippingAddress': buyer.pop('billingAddress')
        })

        print('Value of payer is {}'.format(payer))
        print('Value of buyer is {}'.format(buyer))

        response = self.payu.submit_transaction(
            'a6ab07a8-2bc6-4c39-9ad1-cc18d6d53bf8',
            'payment_test_00000001',
            'payment test',
            'http://localhost',
            100,
            'juan@lopez.com',
            device_id,
            ip_address,
            cookie,
            user_agent,
            payer=payer,
            buyer=buyer
        )
        self.assertTrue(response.get('code'))
        self.assertEqual(response.get('code'), 'SUCCESS')

        self.assertTrue(response.get('transactionResponse'))

        transactionResponse = response.get('transactionResponse')
        self.assertEqual(response.get('code'), 'SUCCESS')
        self.assertTrue(transactionResponse.get('transactionId'))

        self.assertTrue(re.search(
            '[\W\d-]+',
            transactionResponse.get('transactionId'))
        )

    def test_order_detail(self):
        response = self.payu.order_detail(5920900)

        self.assertTrue(response.get('code'))
        self.assertEqual(response.get('code'), 'SUCCESS')


if __name__ == '__main__':
    unittest.main()
