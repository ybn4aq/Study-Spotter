# Generated by Django 4.2.5 on 2023-10-23 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_likes_votes_alter_studyspot_like_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='studyspot',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
