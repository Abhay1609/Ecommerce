# Generated by Django 4.1.2 on 2022-11-19 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password2',
            field=models.CharField(default=345, max_length=40),
            preserve_default=False,
        ),
    ]
