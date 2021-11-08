from cloud.services.daos import VMTagDAO
from cloud.services.entities import VirtualMachineEntity

from cloud.models import VirtualMachine


class VirtualMachineDAO:
    @staticmethod
    def delete_all_records():
        VirtualMachine.objects.all().delete()

    @staticmethod
    def create_or_update_virtual_machine(entity: VirtualMachineEntity) -> VirtualMachine:
        vm, _ = VirtualMachine.objects.get_or_create(
            vm_id=entity.vm_id,
            defaults={'name': entity.name},
        )
        tags = []
        for t in entity.tags:
            tag = VMTagDAO.get_or_create_tag(t)
            tags.append(tag)
        vm.tags.add(*tags)

    @staticmethod
    def get_tags_by_machine_id(machine_id: str) -> set:
        return set(VirtualMachine.objects.get(pk=machine_id).tags.all().values_list('name', flat=True))

    @staticmethod
    def is_machine_exists(machine_id: str) -> bool:
        return VirtualMachine.objects.filter(pk=machine_id).exists()

    @staticmethod
    def get_machines_by_tag_list(tags: set, exclude_machine_id: str) -> set:
        return set(VirtualMachine.objects.filter(
            tags__name__in=tags
        ).exclude(pk=exclude_machine_id).values_list('pk', flat=True))

    @staticmethod
    def get_vms_count() -> int:
        return VirtualMachine.objects.count()
