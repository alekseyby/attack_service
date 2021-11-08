from cloud.models import CloudFirewallRule

from cloud.services.entities import FirewallRuleEntity
from .tag import VMTagDAO


class FireWallRuleDAO:
    @staticmethod
    def delete_all_records():
        CloudFirewallRule.objects.all().delete()

    @staticmethod
    def create_or_update_rule(entity: FirewallRuleEntity) -> CloudFirewallRule:
        source_tag = VMTagDAO.get_or_create_tag(entity.source_tag)
        dest_tag = VMTagDAO.get_or_create_tag(entity.dest_tag)
        CloudFirewallRule.objects.update_or_create(
            fw_id=entity.fw_id,
            defaults=dict(source_tag=source_tag,
                          dest_tag=dest_tag)
        )

    @staticmethod
    def get_possible_accessed_tags_by_tags(tags: set) -> set:
        return set(CloudFirewallRule.objects.filter(source_tag__name__in=tags).values_list('dest_tag__name', flat=True))
