from typing import Type, List

from api.models import APIStat

from cloud.services.readers import IFileReader, JSONFileReader
from cloud.services.daos import (
    VMTagDAO,
    FireWallRuleDAO,
    VirtualMachineDAO,
)
from cloud.services.entities import FirewallRuleEntity, VirtualMachineEntity
from cloud.services.helpers import progressBar


class LoadInfrastructureUsecase:
    def __init__(self, is_delete_old: bool = False) -> None:
        self.is_delete_old = is_delete_old

    def _get_reader(self, filename) -> Type[IFileReader]:
        if filename.endswith('.json'):
            return JSONFileReader

        raise NotImplementedError("We're supporting only json files")

    def _get_entities_from_file(self, filename: str) -> (List[VirtualMachineEntity], List[FirewallRuleEntity]):
        reader = self._get_reader(filename)
        return reader.file_content_to_entities(filename)

    def _delete_current_infrastructure(self):
        for dao in [VMTagDAO,
                    FireWallRuleDAO,
                    VirtualMachineDAO]:
            dao.delete_all_records()

    def _delete_old_stats(self):
        APIStat.objects.all().delete()

    def execute(self, filename) -> None:
        machines, rules = self._get_entities_from_file(filename)
        if self.is_delete_old:
            self._delete_current_infrastructure()
            self._delete_old_stats()
        for machine in progressBar(machines, prefix='Processing machines'):
            VirtualMachineDAO.create_or_update_virtual_machine(machine)

        for rule in progressBar(rules, prefix='Processing rules'):
            FireWallRuleDAO.create_or_update_rule(rule)
