import mock
import pytest
import os
from django.test import TestCase, Client
from cloud.services.cloud_relation_manager import CloudRelationManager
from cloud.services.usecases import LoadInfrastructureUsecase
from api.tests.helpers.test_helpers import create_vm, delete_vm, create_vm_mapping_from_json_data, ATTACK_URL

DIR_PATH = os.path.dirname(os.path.abspath(__file__))


class AttackApiTestCase(TestCase):

    """ Test module for GET /attack endpoint """

    def setUp(self):
        create_vm('test_vm')

    def tearDown(self):
        delete_vm('test_vm')

    @mock.patch('cloud.services.cloud_relation_manager.CloudRelationManager.'
                'get_machines_who_can_possible_access_the_vm_by_vm_id',
                return_value=['a', 'b', ])
    def test_valid_request(self, manager_mock):

        """Request with valid data, returns 200 OK and data"""

        resp = self.client.get(ATTACK_URL, {'vm_id': 'test_vm'})
        self.assertEqual(manager_mock.call_count, 1)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, ['a', 'b'])

    def test_wrong_vm_id(self):

        """Request with wrong vm_id, returns 400 error and information message"""

        resp = self.client.get(ATTACK_URL, {'vm_id': 'unknown_vm'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data, {'vm_id': ['vm not found']})

    def test_empty_required_field(self):

        """Request without vm_id field, returns 400 error and information message"""

        resp = self.client.get(ATTACK_URL)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data, {'vm_id': ['This field is required.']})

    def test_api_stats_not_allowed_methods(self):

        """
        Test GET/attack endpoint allows only GET request
        """

        resp = self.client.post(ATTACK_URL)
        self.assertEqual(resp.status_code, 405, f'Test failed, POST request response status code {resp.status_code}')
        resp = self.client.put(ATTACK_URL)
        self.assertEqual(resp.status_code, 405, f'Test failed, PUT request response status code  {resp.status_code}')
        resp = self.client.patch(ATTACK_URL)
        self.assertEqual(resp.status_code, 405, f'Test failed, PATCH request response status code  {resp.status_code}')
        resp = self.client.delete(ATTACK_URL)
        self.assertEqual(resp.status_code, 405, f'Test failed, DELETE request response status code  {resp.status_code}')


@pytest.fixture()
def preconditions():
    # Add preconditions if it needed
    yield
    # Teardown
    CloudRelationManager().delete_all_vms()


class TestApiAttackSuite:

    """ Test module for validation GET/attack endpoint """

    # Data for parameterization input data for test fixture
    test_data_inputs = [
        DIR_PATH + f'/data_inputs/input-{number}.json' for number in range(0, 4)
    ]

    @pytest.mark.django_db
    @pytest.mark.parametrize('test_path', test_data_inputs)
    def test_attack_endpoint_via_http_requests(self, test_path, preconditions):

        """ Test GET/attack validation routing rules via http requests """

        vms, _, _, vms_mapping = create_vm_mapping_from_json_data(test_path)
        client = Client()
        for vm in vms:
            response = client.get(ATTACK_URL + f'?vm_id={vm.vm_id}')
            assert response.status_code == 200
            response_data = response.json()
            data = vms_mapping.get(vm.vm_id, [])
            for vm_id in response_data:
                assert vm_id in data, f'VM_id: {vm.vm_id} should has access to the next vms:' \
                                      f' {data}, but has access to: {response_data}'

    @pytest.mark.django_db
    @pytest.mark.parametrize('test_path', test_data_inputs)
    def test_vm_routing_by_rules(self, test_path, preconditions):

        """ Test GET/attack validating routing rules via ORM """

        LoadInfrastructureUsecase(is_delete_old=True).execute(test_path)
        vms = CloudRelationManager().get_all_vms()
        for vm in vms:
            vm_id = vm.get('vm_id')
            fact_access_vms = CloudRelationManager().get_machines_who_can_possible_access_the_vm_by_vm_id(vm_id)
            possible_accessed_machines = CloudRelationManager().get_accessable_machines(vm_id)
            if vm_id in fact_access_vms:
                fact_access_vms.remove(vm_id)
            assert possible_accessed_machines == fact_access_vms, f'VM_id:{vm_id} should has access to the next vms: ' \
                                                                  f' {possible_accessed_machines}, but has access to:' \
                                                                  f' {fact_access_vms} '
