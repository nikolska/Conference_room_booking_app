# Generated by Django 2.2.17 on 2021-01-29 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('comment', models.TextField(blank=True)),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Room')),
            ],
            options={
                'unique_together': {('room_id', 'date')},
            },
        ),
    ]
