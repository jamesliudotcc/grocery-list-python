# Generated by Django 2.1.4 on 2019-02-25 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0006_auto_20190225_1850'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='house',
            name='lists_house_name_5f400b_idx',
        ),
    ]
