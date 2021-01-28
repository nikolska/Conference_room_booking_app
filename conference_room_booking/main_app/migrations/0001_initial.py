# Generated by Django 2.2.17 on 2021-01-28 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('capacity', models.PositiveIntegerField(default=0)),
                ('projector', models.BooleanField(default=False)),
            ],
        ),
    ]
