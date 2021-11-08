import json

from typing import List

from cloud.services.entities import VirtualMachineEntity, FirewallRuleEntity

from .i_reader import IFileReader


class JSONFileReader(IFileReader):
    @staticmethod
    def file_to_dict(filename: str) -> dict:
        with open(filename) as file_obj:
            data = json.load(file_obj)
        return data

    @classmethod
    def file_content_to_entities(cls, filename: str) -> (List[VirtualMachineEntity], List[FirewallRuleEntity]):
        data = cls.file_to_dict(filename)
        machines = []
        rules = []
        for machine_data in data['vms']:
            machines.append(VirtualMachineEntity(
                vm_id=machine_data['vm_id'],
                name=machine_data['name'],
                tags=machine_data['tags']
            ))
        for rule_data in data['fw_rules']:
            rules.append(FirewallRuleEntity(
                fw_id=rule_data['fw_id'],
                source_tag=rule_data['source_tag'],
                dest_tag=rule_data['dest_tag'],
            ))
        return machines, rules
