# Generated by Django 4.2.6 on 2023-11-13 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_studyspot_latitude_alter_studyspot_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studyspot',
            name='latitude',
            field=models.CharField(blank=True, default='0', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='studyspot',
            name='longitude',
            field=models.CharField(blank=True, default='0', max_length=200, null=True),
        ),
    ]
