# Generated by Django 2.1 on 2019-02-12 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerView',
            fields=[
                ('campaign_id', models.AutoField(primary_key=True, serialize=False)),
                ('campaign_subject', models.CharField(max_length=500)),
                ('campaign_description', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='EmailActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_opened', models.BooleanField(default=False)),
                ('email_clicked', models.BooleanField(default=False)),
                ('email_delivered', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='EmailsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=1000)),
                ('user_mail_id', models.EmailField(max_length=254)),
                ('from_mail_id', models.EmailField(default='bk78196@gmail.com', max_length=254)),
                ('sent_datetime', models.DateTimeField(auto_now=True)),
                ('user_name', models.CharField(max_length=255)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='notify.CustomerView')),
                ('email_activity', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='notify.EmailActivity')),
            ],
        ),
        migrations.CreateModel(
            name='EmailsUnsubscribed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.EmailField(max_length=254)),
                ('unsubscribed', models.BooleanField(default=False)),
            ],
        ),
    ]
