# Generated by Django 3.1.6 on 2021-04-06 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210406_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rule',
            name='frequency',
            field=models.CharField(choices=[('YEARLY', 'Yearly'), ('MONTHLY', 'Monthly'), ('WEEKLY', 'Weekly'), ('DAILY', 'Daily'), ('HOURLY', 'Hourly'), ('MINUTELY', 'Minutely'), ('SECONDLY', 'Secondly')], default='WEEKLY', max_length=50),
        ),
    ]