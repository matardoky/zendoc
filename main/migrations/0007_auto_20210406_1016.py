# Generated by Django 3.1.6 on 2021-04-06 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rule_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rule',
            name='frequency',
            field=models.CharField(choices=[('', ''), ('YEARLY', 'Yearly'), ('MONTHLY', 'Monthly'), ('WEEKLY', 'Weekly'), ('DAILY', 'Daily'), ('HOURLY', 'Hourly'), ('MINUTELY', 'Minutely'), ('SECONDLY', 'Secondly')], default='', max_length=50),
        ),
    ]