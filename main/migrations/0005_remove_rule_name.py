# Generated by Django 3.1.6 on 2021-04-05 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rule_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rule',
            name='name',
        ),
    ]