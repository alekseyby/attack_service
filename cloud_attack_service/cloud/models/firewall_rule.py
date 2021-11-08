from django.db import models


class CloudFirewallRule(models.Model):
    fw_id = models.CharField(max_length=255, primary_key=True)
    source_tag = models.ForeignKey('cloud.VMTag', on_delete=models.CASCADE, related_name='source_rules')
    dest_tag = models.ForeignKey('cloud.VMTag', on_delete=models.CASCADE, related_name='dest_rules')
