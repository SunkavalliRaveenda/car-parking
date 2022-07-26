# Generated by Django 3.2.10 on 2022-07-22 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slot_api', '0006_auto_20220719_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('occupied', 'Occupied')], default='available', max_length=10),
        ),
        migrations.AlterField(
            model_name='slot',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('occupied', 'Occupied')], default='available', max_length=10),
        ),
    ]
