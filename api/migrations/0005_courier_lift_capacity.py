# Generated by Django 3.1.7 on 2021-03-28 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210328_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='courier',
            name='lift_capacity',
            field=models.IntegerField(default=0),
        ),
    ]