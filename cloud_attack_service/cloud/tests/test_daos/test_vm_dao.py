from django.test import TestCase
from cloud.services.daos import VirtualMachineDAO
from cloud.models import VirtualMachine
from cloud.services.entities import VirtualMachineEntity


class VirtualMachineDAOTestCase(TestCase):
    def _create_vm(self, name, tags=None):
        return VirtualMachine.objects.create(pk=name, name=name)

    def test__delete_everything(self):
        self._create_vm('1')
        self._create_vm('2')
        self._create_vm('3')
        self.assertEqual(VirtualMachine.objects.count(), 3)
        VirtualMachineDAO.delete_all_records()
        self.assertEqual(VirtualMachine.objects.count(), 0)

    def test_create_or_update_virtual_machine(self):
        entity = VirtualMachineEntity(
            vm_id='1',
            name='2',
            tags=['3', '4']
        )
        VirtualMachineDAO.create_or_update_virtual_machine(entity)
        VirtualMachineDAO.create_or_update_virtual_machine(entity)
        self.assertEqual(VirtualMachine.objects.count(), 1)
        vm = VirtualMachine.objects.first()
        self.assertEqual(vm.vm_id, '1')
        self.assertEqual(vm.name, '2')
        self.assertEqual(set(vm.tags.values_list('name', flat=True)), {'3', '4'})

    def test_get_tags_by_machine_id(self):
        entity = VirtualMachineEntity(
            vm_id='1',
            name='2',
            tags=['3', '4']
        )
        VirtualMachineDAO.create_or_update_virtual_machine(entity)
        self.assertSetEqual(VirtualMachineDAO.get_tags_by_machine_id('1'), {'3', '4'})

    def test_is_machine_exists(self):
        entity = VirtualMachineEntity(
            vm_id='1',
            name='2',
            tags=['3', '4']
        )
        VirtualMachineDAO.create_or_update_virtual_machine(entity)

        self.assertTrue(VirtualMachineDAO.is_machine_exists('1'))
        self.assertFalse(VirtualMachineDAO.is_machine_exists('1111'))

    def test_get_machines_by_tag_list(self):
        VirtualMachineDAO.create_or_update_virtual_machine(VirtualMachineEntity(vm_id='1', name='1', tags=['1', '2']))
        VirtualMachineDAO.create_or_update_virtual_machine(VirtualMachineEntity(vm_id='2', name='2', tags=['1', '2']))
        VirtualMachineDAO.create_or_update_virtual_machine(VirtualMachineEntity(vm_id='3', name='3', tags=['3', '4']))
        VirtualMachineDAO.create_or_update_virtual_machine(VirtualMachineEntity(vm_id='5', name='5', tags=['5', '6']))
        machines = VirtualMachineDAO.get_machines_by_tag_list({'1', '2', '3'}, exclude_machine_id='2')
        self.assertSetEqual(machines, {'1', '3'})

    def test_get_vms_count(self):
        self._create_vm('1')
        self._create_vm('2')
        self._create_vm('3')
        self._create_vm('4')
        self.assertEqual(VirtualMachineDAO.get_vms_count(), 4)
