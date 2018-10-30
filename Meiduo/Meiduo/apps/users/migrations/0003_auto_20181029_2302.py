# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-10-29 15:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('areas', '0001_initial'),
        ('users', '0002_user_email_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=20)),
                ('receiver', models.CharField(max_length=10)),
                ('place', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=11)),
                ('tel', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_addr', to='areas.Area')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='district_addr', to='areas.Area')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='province_addr', to='areas.Area')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tb_address',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='default_address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_addr', to='users.Address'),
        ),
    ]
