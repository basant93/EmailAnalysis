from django.db import models
from django.conf import settings
# Create your models here.

class EmailsInfo(models.Model):
    subject = models.CharField(max_length=1000)
    user_mail_id = models.EmailField()
    from_mail_id = models.EmailField(default=settings.EMAIL_HOST_USER)
    sent_datetime = models.DateTimeField(auto_now=True)
    user_name = models.CharField(max_length=255)


class EmailActivity(models.Model):
    email_opened = models.BooleanField(default=False)
    email_clicked = models.BooleanField(default=False)
    email_delivered = models.BooleanField(default=False)
    email_unsubscribed = models.BooleanField(default=False)


class CustomerView(models.Model):
    campaign_id = models.AutoField(primary_key=True)
    customer_email = models.OneToOneField(EmailsInfo, on_delete=models.SET_NULL, null=True)
    customer_activity = models.OneToOneField(EmailActivity, on_delete=models.SET_NULL, null=True)
