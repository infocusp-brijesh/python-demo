# Generated by Django 5.0.7 on 2024-07-16 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='deleted_at',
            field=models.DateTimeField(null=True),
        ),
    ]
