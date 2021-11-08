import mock

from django.test import TestCase
from rest_framework.reverse import reverse
from cloud.models import VirtualMachine


class AttackApiTestCase(TestCase):
    url = reverse('attack')

    def setUp(self) -> None:
        self._create_vm('test_vm')

    def _create_vm(self, name):
        return VirtualMachine.objects.create(pk=name, name=name)

    def test__api_returns_400_if_vm_not_found(self):
        resp = self.client.get(self.url, {'vm_id': 'unknown_vm'})
        self.assertEqual(resp.status_code, 400)

    def test__api_returns_400_if_vm_is_not_passed(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 400)

    @mock.patch('cloud.services.cloud_relation_manager.CloudRelationManager.get_accessable_machines',
                return_value=['a', 'b', ])
    def test_api_service_is_called_if_everything_is_ok(self, manager_mock):
        resp = self.client.get(self.url, {'vm_id': 'test_vm'})
        self.assertEqual(manager_mock.call_count, 1)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, ['a', 'b'])
