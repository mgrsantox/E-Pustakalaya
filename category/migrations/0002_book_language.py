# Generated by Django 2.1 on 2018-09-21 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.CharField(default='English', max_length=200),
            preserve_default=False,
        ),
    ]
