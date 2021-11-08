from django.test import TestCase
from cloud.services.daos import FireWallRuleDAO
from cloud.models import CloudFirewallRule, VMTag
from cloud.services.entities import FirewallRuleEntity


class FirewallRuleDAOTestCase(TestCase):
    def _create_fw(self, t1, t2):
        t1 = VMTag.objects.create(name=t1)
        t2 = VMTag.objects.create(name=t2)
        CloudFirewallRule.objects.create(
            pk='{}->{}'.format(t1.name, t2.name),
            source_tag=t1,
            dest_tag=t2
        )

    def test__delete_everything(self):
        self._create_fw('1', '2')
        self._create_fw('3', '4')
        self._create_fw('5', '6')
        self.assertEqual(CloudFirewallRule.objects.count(), 3)
        FireWallRuleDAO.delete_all_records()
        self.assertEqual(CloudFirewallRule.objects.count(), 0)

    def test_create_or_update_rule__created_and_updated(self):
        entity = FirewallRuleEntity(fw_id='aaa',
                                    source_tag='bbb',
                                    dest_tag='ccc')
        FireWallRuleDAO.create_or_update_rule(entity)
        self.assertEqual(CloudFirewallRule.objects.count(), 1)
        rule = CloudFirewallRule.objects.first()
        self.assertEqual(rule.source_tag.name, 'bbb')
        self.assertEqual(rule.dest_tag.name, 'ccc')
        entity.source_tag = 'qqq'
        entity.dest_tag = 'eee'
        FireWallRuleDAO.create_or_update_rule(entity)
        self.assertEqual(CloudFirewallRule.objects.count(), 1)
        rule = CloudFirewallRule.objects.first()
        self.assertEqual(rule.source_tag.name, 'qqq')
        self.assertEqual(rule.dest_tag.name, 'eee')

    def get_possible_accessed_tags_by_tags(self):
        self._create_fw('a', 'b')
        self._create_fw('a', 'c')
        self._create_fw('a', 'd')
        self._create_fw('q', 'w')
        self._create_fw('e', 'r')

        possible_accessed = FireWallRuleDAO.get_possible_accessed_tags_by_tags({'a', 'q'})
        self.assertSetEqual(possible_accessed, {'b', 'c', 'd', 'w'})
