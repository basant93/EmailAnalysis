# Generated by Django 2.1 on 2019-02-12 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notify', '0002_auto_20190212_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerview',
            name='campaign_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='notify.Category'),
        ),
    ]
