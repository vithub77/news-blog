# Generated by Django 5.0.6 on 2024-05-13 14:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsBdEn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=500)),
                ('description', models.TextField(default='')),
                ('url', models.CharField(max_length=500)),
                ('data', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CommentsEn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100)),
                ('text', models.TextField(default='')),
                ('publication_date', models.DateTimeField(auto_now_add=True)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.newsbd')),
            ],
        ),
    ]