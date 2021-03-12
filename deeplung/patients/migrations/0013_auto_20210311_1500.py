# Generated by Django 3.1.7 on 2021-03-11 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0012_modelimages'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='modelimages',
            options={'ordering': ['position']},
        ),
        migrations.AlterField(
            model_name='patient',
            name='alive',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='smoker',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
