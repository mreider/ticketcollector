# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-12 05:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('collection_id', models.AutoField(primary_key=True, serialize=False)),
                ('search_criteria', models.CharField(max_length=2000, null=True)),
                ('name', models.CharField(max_length=1000, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CollectionDocTicket',
            fields=[
                ('collection_doc_ticket_id', models.AutoField(primary_key=True, serialize=False)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doc_collection', to='app.Collection')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('zd_comment_id', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField()),
                ('plain_body', models.TextField()),
                ('is_public', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_id', models.AutoField(primary_key=True, serialize=False)),
                ('zd_ticket_id', models.CharField(max_length=1000)),
                ('subject', models.CharField(max_length=1000)),
                ('requester', models.CharField(max_length=1000)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_collection', to='app.Collection')),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_ticket', to='app.Ticket'),
        ),
        migrations.AddField(
            model_name='collectiondocticket',
            name='ticket',
            field=models.ManyToManyField(related_name='doc_tickets', to='app.Ticket'),
        ),
    ]
