# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20150607_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='Featurette',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('heading', models.CharField(max_length=255)),
                ('muted_heading', models.CharField(max_length=255, blank=True)),
                ('lead_text', models.TextField(blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'uploads/', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeaturettePlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('template', models.CharField(max_length=255, verbose_name=b'Template', choices=[(b'left.html', b'Text on Left'), (b'right.html', b'Text on Right'), (b'alternating.html', b'Alternating')])),
                ('width', models.PositiveIntegerField(default=0, help_text=b'Fixed width in pixels for images. If left empty and height is given, width will be automatically calculated to preserve aspect ratio.', verbose_name=b'Image Width')),
                ('height', models.PositiveIntegerField(default=0, help_text=b'Fixed height in pixels for images. If left empty and width is given, width will be automatically calculated to preserve aspect ratio.', verbose_name=b'Image Height')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AddField(
            model_name='featurette',
            name='featurette',
            field=models.ForeignKey(to='easy_featurette.FeaturettePlugin'),
        ),
    ]
