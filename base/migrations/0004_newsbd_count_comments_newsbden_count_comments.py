# Generated by Django 5.0.6 on 2024-05-14 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_commentsen_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsbd',
            name='count_comments',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='newsbden',
            name='count_comments',
            field=models.IntegerField(default=0),
        ),
    ]
