from cloud.services.daos import VMTagDAO, VirtualMachineDAO, FireWallRuleDAO


class CloudRelationManager:
    def __init__(self):
        self.vm_dao = VirtualMachineDAO()
        self.tag_dao = VMTagDAO()
        self.rule_dao = FireWallRuleDAO()

    def _get_possible_accessed_tags_by_tags(self, tags: set) -> set:
        rule_tags = self.rule_dao.get_possible_accessed_tags_by_tags(tags)
        machine_tags = self.tag_dao.get_all_tags_by_accessible_tags(rule_tags)
        return machine_tags

    def get_accessable_machines(self, machine_id: str) -> set:
        original_tags = self.vm_dao.get_tags_by_machine_id(machine_id)
        possible_accessed_tags = self._get_possible_accessed_tags_by_tags(original_tags)
        current_tags = set()
        while len(current_tags) != len(possible_accessed_tags):
            current_tags = possible_accessed_tags
            possible_accessed_tags = current_tags.union(
                self._get_possible_accessed_tags_by_tags(possible_accessed_tags))
        possible_accessed_machines = self.vm_dao.get_machines_by_tag_list(current_tags, exclude_machine_id=machine_id)
        return possible_accessed_machines
