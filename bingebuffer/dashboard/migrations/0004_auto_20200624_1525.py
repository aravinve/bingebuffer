# Generated by Django 3.0.7 on 2020-06-24 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20200624_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
