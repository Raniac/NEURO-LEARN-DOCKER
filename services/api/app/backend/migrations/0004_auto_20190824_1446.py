# Generated by Django 2.2.2 on 2019-08-24 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20190824_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data_demo',
            name='data_id',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='data_demo',
            name='data_name',
            field=models.CharField(max_length=64),
        ),
    ]
