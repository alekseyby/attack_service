import random
from django.test import TestCase
from api.tests.helpers.test_helpers import create_vm, STATS_URL, ATTACK_URL
from cloud.services.cloud_relation_manager import CloudRelationManager

RANDOM_SUFFIX = random.randint(1, 10)


class StatsApiTestCase(TestCase):
    """ Test module for GET /stats endpoint """

    def tearDown(self):
        CloudRelationManager().delete_all_vms()

    def test_api_stats_returns_valid_response(self):

        """ Test GET/stats base verification"""

        for x in range(RANDOM_SUFFIX):
            create_vm(str(x))
        resp = self.client.get(STATS_URL)
        self.assertEqual(resp.status_code, 200, f'Test failed with response status code {resp.status_code}')
        data = resp.data
        self.assertEqual(data['vm_count'], RANDOM_SUFFIX, f'Test failed, expected vm_count: {RANDOM_SUFFIX},'
                                                          f' observed: {data["vm_count"]}')
        self.assertIn('request_count', data)
        self.assertIn('average_request_time', data)

    def test_api_stats_returns_valid_request_count(self):

        """
        Test GET/stats returns actual "request_count" field after
        GET /attack and GET/stats requests
        """

        create_vm('test_vm')
        for i in range(RANDOM_SUFFIX):
            self.client.get(ATTACK_URL, {'vm_id': 'test_vm'})
        resp = self.client.get(STATS_URL)
        self.assertEqual(resp.status_code, 200, f'Test failed with response status code {resp.status_code}')
        data = resp.data
        self.assertEqual(data['vm_count'], 1, f'Test failed, expected vm_count: 1,'
                                              f' observed: {data["vm_count"]}')
        self.assertEqual(data['request_count'], RANDOM_SUFFIX, f'Test failed, expected request_count: {RANDOM_SUFFIX},'
                                                               f' observed: {data["request_count"]}')
        self.assertIn('average_request_time', data)
        resp = self.client.get(STATS_URL)
        data = resp.data
        self.assertEqual(data['request_count'], RANDOM_SUFFIX+1, f'Test failed, expected request_count:'
                                                                 f' {RANDOM_SUFFIX+1},'
                                                                 f'observed: {data["request_count"]}')

    def test_api_stats_not_allowed_methods(self):

        """
        Test GET/stats endpoint allows only GET request
        """
        resp = self.client.post(STATS_URL)
        self.assertEqual(resp.status_code, 405, f'Test failed, POST request response status code {resp.status_code}')
        resp = self.client.put(STATS_URL)
        self.assertEqual(resp.status_code, 405, f'Test failed, PUT request response status code  {resp.status_code}')
        resp = self.client.patch(STATS_URL)
        self.assertEqual(resp.status_code, 405, f'Test failed, PATCH request response status code  {resp.status_code}')
        resp = self.client.delete(STATS_URL)
        self.assertEqual(resp.status_code, 405, f'Test failed, DELETE request response status code  {resp.status_code}')
