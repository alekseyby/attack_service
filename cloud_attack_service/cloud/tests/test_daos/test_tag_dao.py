from django.test import TestCase
from cloud.services.daos import VMTagDAO
from cloud.models import VMTag, VirtualMachine


class VMTagDAOTestCase(TestCase):
    def _create_tag(self, t1):
        return VMTag.objects.create(name=t1)

    def test__delete_everything(self):
        self._create_tag('1')
        self._create_tag('2')
        self._create_tag('3')
        self.assertEqual(VMTag.objects.count(), 3)
        VMTagDAO.delete_all_records()
        self.assertEqual(VMTag.objects.count(), 0)

    def test_get_or_create_tag(self):
        VMTagDAO.get_or_create_tag('1')
        VMTagDAO.get_or_create_tag('1')
        VMTagDAO.get_or_create_tag('1')
        self.assertEqual(VMTag.objects.count(), 1)
        tag = VMTag.objects.first()
        self.assertEqual(tag.name, '1')

    def test_get_all_tags_by_accessible_tags(self):
        vm = VirtualMachine.objects.create(pk='1', name='2')
        vm.tags.add(self._create_tag('1'))
        vm.tags.add(self._create_tag('2'))
        vm.tags.add(self._create_tag('3'))
        self.assertSetEqual(VMTagDAO.get_all_tags_by_accessible_tags({'1'}), {'1', '2', '3'})
