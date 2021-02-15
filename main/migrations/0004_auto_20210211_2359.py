# Generated by Django 3.1.6 on 2021-02-11 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rule_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='planning',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='planning',
            name='type',
            field=models.CharField(choices=[('RECCURENCE', ' OUVERTURE RECCURENTE'), ('EXCEPTION', 'OUVERTURE EXCEPTIONNELLE')], default='EXCEPTION', max_length=50),
        ),
    ]
