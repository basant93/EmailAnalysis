from django.db import models
from django.conf import settings
# Create your models here.


class EmailActivity(models.Model):
    email_opened = models.BooleanField(default=False)
    email_clicked = models.BooleanField(default=False)
    email_delivered = models.BooleanField(default=False)

class Category(models.Model):
    CATEGORY_CHOICES = [('WELCOME', 'WELCOME'), ('OFFER', 'OFFER'), ('SURVEY', 'SURVEY'), ('REQUEST', 'REQUEST'), \
        ('NEWSLETTER', 'NEWSLETTER'), ('ANOUNCEMENT', 'ANOUNCEMENT')]
    category = models.CharField(max_length=50, choices = CATEGORY_CHOICES, default='WELCOME')

    def __str__(self):
        return self.category

class CustomerView(models.Model):
    campaign_id = models.AutoField(primary_key=True)
    campaign_subject = models.CharField(max_length=500)
    campaign_description = models.CharField(max_length=1000)
    campaign_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)  

    
class EmailsInfo(models.Model):
    subject = models.CharField(max_length=1000)
    user_mail_id = models.EmailField()
    from_mail_id = models.EmailField(default=settings.EMAIL_HOST_USER)
    sent_datetime = models.DateTimeField(auto_now=True)
    user_name = models.CharField(max_length=255)
    customer = models.ForeignKey(CustomerView, on_delete=models.CASCADE, null=True)
    email_activity = models.ForeignKey(EmailActivity, on_delete=models.SET_NULL, null=True)



class EmailsUnsubscribed(models.Model):
    mail = models.EmailField()
    unsubscribed = models.BooleanField(default=False)
    customer = models.ForeignKey(CustomerView, on_delete=models.SET_NULL, null=True)


    
