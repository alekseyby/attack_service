from django.db import models


class VirtualMachine(models.Model):
    vm_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    tags = models.ManyToManyField('cloud.VMTag', related_name='virtual_machines', blank=True)
