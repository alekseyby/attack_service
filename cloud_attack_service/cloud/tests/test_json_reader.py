import mock
from django.test import TestCase
from cloud.services.readers import JSONFileReader


class JSONConverterTestCase(TestCase):
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
    def test_file_content_to_entities_with_valid_json(self, mock):
        vms, rules = JSONFileReader.file_content_to_entities('lalala')
        self.assertEqual(len(vms), 2)
        self.assertEqual(vms[0].name, "jira_server")
        self.assertEqual(vms[0].vm_id, "vm-a211de")
        self.assertEqual(vms[0].tags, ['ci', 'dev'])
        self.assertEqual(vms[1].name, "bastion")
        self.assertEqual(vms[1].vm_id, "vm-c7bac01a07")
        self.assertEqual(vms[1].tags, ['ssh', 'dev'])
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0].source_tag, 'ssh')
        self.assertEqual(rules[0].dest_tag, 'dev')
