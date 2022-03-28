from collections import defaultdict
from cloud.services.readers import JSONFileReader
from cloud.services.usecases import LoadInfrastructureUsecase
from cloud.models import VirtualMachine
from rest_framework.reverse import reverse


ATTACK_URL = reverse('attack')
STATS_URL = reverse('stats')


def create_vm(name):
    return VirtualMachine.objects.create(pk=name, name=name)


def delete_vm(name):
    VirtualMachine.objects.filter(pk=name).delete()


def create_vm_mapping_from_json_data(path, is_delete_old=True):
    rules_collection = defaultdict(list)
    vms_collection = defaultdict(list)
    vms_mapping = defaultdict(list)
    LoadInfrastructureUsecase(is_delete_old=is_delete_old).execute(path)
    vms, rules = JSONFileReader.file_content_to_entities(path)
    for rule in rules:
        rules_collection[rule.fw_id] = [rule.source_tag, rule.dest_tag]
    for vm in vms:
        vms_collection[vm.vm_id] = [vm.tags]
    route_rules = list(rules_collection.values())
    for vm_name, vm_tags in vms_collection.items():
        for tag in vm_tags[0]:
            for dest_rule_tags in route_rules:
                # if vm tag same as source_tag in rule so find dest_tag
                if dest_rule_tags[0] == tag:
                    destination_tag = dest_rule_tags[1]
                    # find vms with this tag
                    for dest_vm, dest_vm_tags in vms_collection.items():
                        if destination_tag in dest_vm_tags[0]:
                            vms_mapping[vm_name].append(dest_vm)
    return vms, rules_collection, vms_collection, vms_mapping
