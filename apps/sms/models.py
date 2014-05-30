from django.db import models


class SMS(models.Model):

    class Meta:
        verbose_name = 'SMS'
        verbose_name_plural = "SMSes"

    mobile_number = models.CharField(max_length=12)
    delivery_status = models.CharField(max_length=16, default='unknown')
    created = models.DateTimeField(auto_now_add=True)
    message_id = models.CharField(max_length=32, db_index=True,
                                  null=True, blank=True)
