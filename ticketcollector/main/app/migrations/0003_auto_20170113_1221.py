# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-13 06:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20170112_1110'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('zd_comment_id', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField()),
                ('plain_body', models.TextField()),
                ('is_public', models.BooleanField()),
                ('posted_by', models.CharField(max_length=1000)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_ticket', to='app.Ticket')),
            ],
        ),
        migrations.RemoveField(
            model_name='comments',
            name='ticket',
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
    ]
