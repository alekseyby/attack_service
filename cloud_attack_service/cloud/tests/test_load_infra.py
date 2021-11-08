import mock

from django.test import TestCase
from cloud.services.usecases import LoadInfrastructureUsecase
from cloud.models import VirtualMachine, CloudFirewallRule


class LoadInfraTestCase(TestCase):
    @mock.patch('cloud.services.readers.json_reader.JSONFileReader.file_to_dict', return_value={
        "vms": [
            {
                "vm_id": "vm-a211de",
                "name": "jira_server",
                "tags": [
                    "ci",
                    "dev"
                ]
            },
            {
                "vm_id": "vm-c7bac01a07",
                "name": "bastion",
                "tags": [
                    "ssh",
                    "dev"
                ]
            }
        ],
        "fw_rules": [
            {
                "fw_id": "fw-82af742",
                "source_tag": "ssh",
                "dest_tag": "dev"
            }
        ]
    })
    def test_load_infra_from_json_file(self, mock):
        LoadInfrastructureUsecase().execute('lalala.json')
        self.assertEqual(VirtualMachine.objects.count(), 2)
        vm1 = VirtualMachine.objects.get(pk='vm-a211de')
        self.assertEqual(vm1.name, 'jira_server')
        self.assertSetEqual(set(vm1.tags.values_list('name', flat=True)), {'ci', 'dev'})

        vm2 = VirtualMachine.objects.get(pk='vm-c7bac01a07')
        self.assertEqual(vm2.name, 'bastion')
        self.assertSetEqual(set(vm2.tags.values_list('name', flat=True)), {'ssh', 'dev'})

        self.assertEqual(CloudFirewallRule.objects.count(), 1)
        rule = CloudFirewallRule.objects.first()
        self.assertEqual(rule.source_tag.name, 'ssh')
        self.assertEqual(rule.dest_tag.name, 'dev')
