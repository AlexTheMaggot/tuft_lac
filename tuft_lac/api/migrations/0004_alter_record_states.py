# Generated by Django 5.1.1 on 2024-11-05 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_record'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='states',
            field=models.ManyToManyField(to='api.state'),
        ),
    ]
