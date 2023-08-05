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

response = {'pagination': {'count': 2, 'page': 1, 'pages': 1, 'per_page': 20},
 'results': [{'candidate_contributions_less_repayments': 1435680385.69,
              'candidate_id': 'P00000001',
              'candidate_last_name': 'All candidates',
              'candidate_name': 'ALL CANDIDATES',
              'candidate_party_affiliation': None,
              'cash_on_hand_end': 216909831.62,
              'committee_designation': 'P',
              'committee_id': None,
              'committee_name': None,
              'committee_type': None,
              'debts_owed_by_committee': 10672473.66,
              'disbursements_less_offsets': 2428395096.51,
              'election_year': 2020,
              'exempt_legal_accounting_disbursement': 0.0,
              'federal_funds': 0.0,
              'fundraising_disbursements': 236662.51,
              'individual_contributions_less_refunds': 989643942.41,
              'net_receipts': 2637877295.66,
              'offsets_to_operating_expenditures': 38916359.23,
              'operating_expenditures': 2440681926.13,
              'other_disbursements': 26411941.66,
              'pac_contributions_less_refunds': 983057.49,
              'party_contributions_less_refunds': 5565.0,
              'repayments_loans_made_by_candidate': 15667891.42,
              'repayments_other_loans': 580.0,
              'rounded_net_receipts': 2637.9,
              'total_contribution_refunds': 19070819.76,
              'total_loan_repayments_made': 15668471.42,
              'transfers_from_affiliated_committees': 202216000.7,
              'transfers_to_other_authorized_committees': 6251517.66},
             {'candidate_contributions_less_repayments': 69091448.05,
              'candidate_id': 'P00000001',
              'candidate_last_name': 'All candidates',
              'candidate_name': 'ALL CANDIDATES',
              'candidate_party_affiliation': None,
              'cash_on_hand_end': 16412318.79,
              'committee_designation': 'P',
              'committee_id': None,
              'committee_name': None,
              'committee_type': None,
              'debts_owed_by_committee': 3702149.78,
              'disbursements_less_offsets': 1446299929.43,
              'election_year': 2016,
              'exempt_legal_accounting_disbursement': 0.0,
              'federal_funds': 1544964.68,
              'fundraising_disbursements': 16101.68,
              'individual_contributions_less_refunds': 1081052068.78,
              'net_receipts': 1462314770.13,
              'offsets_to_operating_expenditures': 39962259.19,
              'operating_expenditures': 1483952338.17,
              'other_disbursements': 2298748.77,
              'pac_contributions_less_refunds': 2947772.53,
              'party_contributions_less_refunds': 29683.23,
              'repayments_loans_made_by_candidate': 25000.0,
              'repayments_other_loans': 510811.64,
              'rounded_net_receipts': 1462.3,
              'total_contribution_refunds': 24814047.22,
              'total_loan_repayments_made': 535811.64,
              'transfers_from_affiliated_committees': 301668101.25,
              'transfers_to_other_authorized_committees': 4265220.29}]}

class TestPresidentialSummary(unittest.TestCase):
    """PresidentialSummary unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPresidentialSummary(self):
        """Test PresidentialSummary"""
        api_response = api_instance.presidential_financial_summary_get(
            api_key,
            per_page=per_page,
            sort=sort,
            candidate_id=candidate_id)

        self.assertEqual(api_response, response)
