# Generated by Django 3.1.6 on 2021-04-15 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_calendar_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address1',
            field=models.CharField(default='main', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='address2',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(default='main', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='zip_code',
            field=models.CharField(default='main', max_length=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='title',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='occurrence',
            name='title',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]