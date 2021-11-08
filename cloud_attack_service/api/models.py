from django.db import models


class APIStat(models.Model):
    requested_at = models.DateTimeField(auto_now=True)
    response_time = models.DecimalField(db_index=True, decimal_places=7, max_digits=9)
