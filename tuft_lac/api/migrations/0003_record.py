# Generated by Django 5.1.1 on 2024-11-05 06:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.machine')),
                ('states', models.ManyToManyField(blank=True, null=True, to='api.state')),
            ],
        ),
    ]
