# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gifts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('contrib_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('value', models.DecimalField(decimal_places=2, max_digits=7)),
                ('contributed_by', models.ForeignKey(related_name='contributed_gifts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='gift',
            name='contrib_sum',
            field=models.DecimalField(decimal_places=2, max_digits=7, default=0),
        ),
        migrations.AlterField(
            model_name='gift',
            name='bought_by',
            field=models.ForeignKey(null=True, blank=True, related_name='bought_gifts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contribution',
            name='gift',
            field=models.ForeignKey(related_name='contributions', to='gifts.Gift'),
        ),
    ]
