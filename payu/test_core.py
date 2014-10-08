import unittest
from payu import PayU


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
        response = self.payu.get_tokens('10', 'a6ab07a8-2bc6-4c39-9ad1-cc18d6d53bf8')
        self.assertTrue(response.get('code'))
        self.assertEqual(response.get('code'), 'SUCCESS')

    def test_submit_transaction(self):
        response = self.payu.submit_transaction(
            'a6ab07a8-2bc6-4c39-9ad1-cc18d6d53bf8',
            'payment_test_00000001',
            'payment test',
            'http://localhost',
            100,
            'juan@lopez.com'
        )
        self.assertTrue(response.get('code'))
        self.assertEqual(response.get('code'), 'SUCCESS')

        self.assertTrue(response.get('transactionResponse'))

        transactionResponse = response.get('transactionResponse')
        self.assertEqual(response.get('code'), 'SUCCESS')
        self.assertTrue(transactionResponse.get('transactionId'))
        self.assertRegexpMatches(transactionResponse.get('transactionId'), '[\W\d-]+')

    def test_order_detail(self):
        response = self.payu.order_detail(5920900)

        self.assertTrue(response.get('code'))
        self.assertEqual(response.get('code'), 'SUCCESS')


if __name__ == '__main__':
    unittest.main()
