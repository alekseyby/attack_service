from django.test import TestCase
from rest_framework.reverse import reverse
from cloud.models import VirtualMachine


class StatApiTestCase(TestCase):
    url = reverse('stats')

    def _create_vm(self, name):
        return VirtualMachine.objects.create(pk=name, name=name)

    def test__api_returns_valid_response(self):
        for x in range(5):
            self._create_vm(str(x))

        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.data
        self.assertEqual(data['vm_count'], 5)
        self.assertIn('request_count', data)
        self.assertIn('average_request_time', data)
