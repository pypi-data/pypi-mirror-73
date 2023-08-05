from xml.etree.ElementTree import fromstring

from .base_integration_test import BaseIntegrationTest
from platron.request.clients.post_client import PostClient
from platron.request.request_builders.get_status_builder import GetStatusBuilder
from platron.request.request_builders.init_payment_builder import InitPaymentBuilder


class GetStatusTest(BaseIntegrationTest):

    def test_create_transaction_chain(self):
        client = PostClient(self.get_merchant_id(), self.get_secret_key())
        builder = InitPaymentBuilder('10.00', 'test')
        result = client.request(builder)
        root = fromstring(result)
        pg_payment_id = root.find('pg_payment_id').text

        builder = GetStatusBuilder(pg_payment_id)

        self.assertIsNotNone(client.request(builder))
