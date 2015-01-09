# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Battlelog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('winner', models.CharField(max_length=100, choices=[(b'attacker', b'attacker'), (b'defender', b'defender')])),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lastseen', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first', models.CharField(default=b'', max_length=100, blank=True)),
                ('last', models.CharField(default=b'', max_length=100, blank=True)),
                ('nickname', models.CharField(default=b'', unique=True, max_length=100, blank=True)),
                ('wins', models.IntegerField(default=0)),
                ('losses', models.IntegerField(default=0)),
                ('winstreak', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lastseen', models.DateTimeField(auto_now=True)),
                ('highlighted', models.TextField()),
                ('owner', models.ForeignKey(related_name='players', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='battlelog',
            name='attacker',
            field=models.ForeignKey(related_name='attacker', to='battlelogs.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='battlelog',
            name='defender',
            field=models.ForeignKey(related_name='defender', to='battlelogs.Player'),
            preserve_default=True,
        ),
    ]
