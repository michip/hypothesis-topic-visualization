# Generated by Django 3.1.3 on 2020-11-10 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20201110_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.TextField(blank=True),
        ),
    ]
