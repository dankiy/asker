# Generated by Django 2.2 on 2019-12-22 02:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20191222_0222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='votes',
            field=models.ManyToManyField(blank=True, default=[], null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]