# Generated by Django 3.0.5 on 2021-06-02 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Category name')),
                ('slug', models.SlugField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Genre name')),
                ('slug', models.SlugField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Title name')),
                ('year', models.IntegerField(blank=True, null=True, verbose_name='Title year')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Title description')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Category')),
                ('genre', models.ManyToManyField(blank=True, null=True, to='api.Genre')),
            ],
        ),
    ]
