# Generated by Django 4.2.6 on 2023-11-13 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_studyspot_latitude_alter_studyspot_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studyspot',
            name='latitude',
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='studyspot',
            name='longitude',
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=9),
        ),
    ]
