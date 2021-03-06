# Generated by Django 3.1.3 on 2020-11-09 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_identifier', models.CharField(max_length=500, unique=True)),
                ('url', models.CharField(max_length=500)),
                ('doi', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=500)),
                ('text', models.TextField()),
                ('data', models.DateField()),
                ('type', models.CharField(choices=[('tweet', 'Twitter')], max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentInTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('probability', models.FloatField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.topic')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.document')),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='tags',
            field=models.ManyToManyField(related_name='documents', to='core.Tag'),
        ),
    ]
