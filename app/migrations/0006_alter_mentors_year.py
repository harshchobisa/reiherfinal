# Generated by Django 3.2.2 on 2021-05-09 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_mentees_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentors',
            name='year',
            field=models.IntegerField(),
        ),
    ]
