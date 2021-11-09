from django.test import TestCase

from cloud.models import CloudFirewallRule, VMTag, VirtualMachine
from cloud.services.cloud_relation_manager import CloudRelationManager


class CloudRelationManagerTestCase(TestCase):
    def _create_fw(self, t1, t2):
        t1, _ = VMTag.objects.get_or_create(name=t1)
        t2, _ = VMTag.objects.get_or_create(name=t2)
        CloudFirewallRule.objects.create(
            pk='{}->{}'.format(t1.name, t2.name),
            source_tag=t1,
            dest_tag=t2
        )

    def _create_vm(self, pk, name, tags):
        vm = VirtualMachine.objects.create(pk=pk, name=name)
        for t in tags:
            t, _ = VMTag.objects.get_or_create(name=t)
            vm.tags.add(t)

    def test_simple_rule_relation_1_to_1(self):
        self._create_vm(pk='aaa', name='111', tags=['a', 'b'])
        self._create_vm(pk='bbb', name='222', tags=['c', 'd'])
        self._create_fw('a', 'c')

        self.assertSetEqual(
            CloudRelationManager().get_accessable_machines('aaa'),
            {'bbb'}
        )

    def test_access_to_the_same_tag_without_rule(self):
        self._create_vm(pk='aaa', name='111', tags=['a', 'b'])
        self._create_vm(pk='bbb', name='222', tags=['a', 'b'])
        self.assertSetEqual(
            CloudRelationManager().get_accessable_machines('aaa'),
            set()
        )

    def test_access_to_the_same_tag_with_rule(self):
        self._create_vm(pk='aaa', name='111', tags=['a', 'b'])
        self._create_vm(pk='bbb', name='222', tags=['a', 'b'])
        self._create_fw('a', 'a')
        self.assertSetEqual(
            CloudRelationManager().get_accessable_machines('aaa'),
            {'bbb'}
        )

    def test_access_to_infra_chain(self):
        self._create_vm(pk='aaa', name='111', tags=['a', 'b'])
        self._create_vm(pk='bbb', name='222', tags=['c', 'd'])
        self._create_vm(pk='ccc', name='333', tags=['e', 'f'])
        self._create_vm(pk='ddd', name='444', tags=['q', 'w'])
        self._create_fw('a', 'd')
        self._create_fw('c', 'f')
        self._create_fw('e', 'w')
        self.assertSetEqual(
            CloudRelationManager().get_accessable_machines('aaa'),
            {'bbb', 'ccc', 'ddd'}
        )

    def test_get_possible_attackers_1_to_1(self):
        self._create_vm(pk='aaa', name='111', tags=['a', 'b'])
        self._create_vm(pk='bbb', name='222', tags=['c', 'd'])
        self._create_fw('a', 'c')

        self.assertSetEqual(
            CloudRelationManager().get_machines_who_can_possible_access_the_vm_by_vm_id('bbb'),
            {'aaa'}
        )

    def test_get_possible_attackers_to_the_same_tag_without_rule(self):
        self._create_vm(pk='aaa', name='111', tags=['a', 'b'])
        self._create_vm(pk='bbb', name='222', tags=['a', 'b'])
        self.assertSetEqual(
            CloudRelationManager().get_machines_who_can_possible_access_the_vm_by_vm_id('bbb'),
            set()
        )

    def test_get_possible_attackers_to_the_same_tag_with_rule(self):
        self._create_vm(pk='aaa', name='111', tags=['a', 'b'])
        self._create_vm(pk='bbb', name='222', tags=['a', 'b'])
        self._create_fw('a', 'a')
        self.assertSetEqual(
            CloudRelationManager().get_accessable_machines('aaa'),
            {'bbb'}
        )

    def test_get_possible_attackers_to_infra_chain(self):
        self._create_vm(pk='aaa', name='111', tags=['a', 'b'])
        self._create_vm(pk='bbb', name='222', tags=['c', 'd'])
        self._create_vm(pk='ccc', name='333', tags=['e', 'f'])
        self._create_vm(pk='ddd', name='444', tags=['q', 'w'])
        self._create_vm(pk='eee', name='555', tags=['b', 'f'])
        self._create_fw('a', 'd')
        self._create_fw('c', 'f')
        self._create_fw('e', 'w')
        self.assertSetEqual(
            CloudRelationManager().get_machines_who_can_possible_access_the_vm_by_vm_id('ddd'),
            {'bbb', 'ccc', 'aaa'}
        )
