# Generated by Django 3.1.7 on 2021-03-28 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210328_2148'),
    ]

    operations = [
        migrations.RenameField(
            model_name='delivering',
            old_name='courier',
            new_name='courier_id',
        ),
        migrations.RenameField(
            model_name='delivering',
            old_name='order',
            new_name='order_id',
        ),
    ]
