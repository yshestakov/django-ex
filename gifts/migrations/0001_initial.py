# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gift',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(max_digits=7, decimal_places=2)),
                ('reg_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('bought_date', models.DateTimeField(blank=True, null=True)),
                ('bought_by', models.ForeignKey(related_name='bought_gifts', to=settings.AUTH_USER_MODEL, null=True)),
                ('wished_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='wished_gifts')),
            ],
        ),
    ]
