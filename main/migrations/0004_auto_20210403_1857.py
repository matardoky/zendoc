# Generated by Django 3.1.6 on 2021-04-03 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210403_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.CharField(choices=[('OUVERTURE RECCURENTE', 'OUVERTURE RECCURENTE'), ('OUVERTURE EXCEPTIONNELLE', 'OUVERTURE EXCEPTIONNELLE')], default='OUVERTURE RECCURENTE', max_length=50),
        ),
    ]
