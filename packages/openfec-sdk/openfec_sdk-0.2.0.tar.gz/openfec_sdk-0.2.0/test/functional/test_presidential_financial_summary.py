import openfec_sdk
import unittest
from pprint import pprint
import os
from test.configuration import setup_testing_environment


setup_testing_environment()
API_KEY = os.getenv('API_KEY')

configuration = openfec_sdk.Configuration()
configuration.api_key['api_key'] = API_KEY

# create an instance of the API class
api_instance = openfec_sdk.PresidentialApi(openfec_sdk.ApiClient(configuration))
api_key = API_KEY
per_page = 20 # int | The number of results returned per page. Defaults to 20. (optional) (default to 20)
sort = '-net_receipts' # str | Provide a field to sort by. Use - for descending order. (optional) (default to -net_receipts)
candidate_id = ['P00000001'] # list[str] |  A unique identifier assigned to each candidate registered with the FEC. If a person runs for several offices, that person will have separate candidate IDs for each office.   -P00000001    All candidates   -P00000002    Democrasts   -P00000003    Republicans  (optional)

class TestPresidentialSummary(unittest.TestCase):
    """PresidentialSummary unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPresidentialSummary(self):
        """Test PresidentialSummary"""
        pass
        # api_response = api_instance.presidential_financial_summary_get(
        #     api_key,
        #     per_page=per_page,
        #     sort=sort,
        #     candidate_id=candidate_id)

        # self.assertEqual(api_response, response)
