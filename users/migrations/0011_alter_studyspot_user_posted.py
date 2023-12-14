# Generated by Django 4.2.6 on 2023-11-15 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0010_remove_studyspot_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studyspot',
            name='user_posted',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
