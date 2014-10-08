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
        from payu import PayU
        payu = PayU()
        response = payu.get_tokens('10', 'a6ab07a8-2bc6-4c39-9ad1-cc18d6d53bf8')
        self.assertTrue(response.get('code'))
        self.assertEqual(response.get('code'), 'SUCCESS')



if __name__ == '__main__':
    unittest.main()
