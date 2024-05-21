# Generated by Django 5.0.6 on 2024-05-20 21:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_newsbd_count_comments_newsbden_count_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='PosNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=100)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.newsbd')),
            ],
        ),
    ]