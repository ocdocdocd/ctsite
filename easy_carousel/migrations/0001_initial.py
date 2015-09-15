# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20150607_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('name', models.CharField(max_length=50, verbose_name=b'Name')),
                ('interval', models.IntegerField(default=5000, help_text=b'The amount of time in milliseconds to delay cycling items. If zero, carousel will not auto-cycle.')),
                ('show_title', models.BooleanField(default=False, help_text=b'Display image titles, if true.')),
                ('show_caption', models.BooleanField(default=False, help_text=b'Display caption text, if true.')),
                ('show_controls', models.BooleanField(default=False, help_text=b'Display carousel controls, if true.')),
                ('show_indicator', models.BooleanField(default=False, help_text=b'Display slide indicator, if true.')),
                ('fill_width', models.BooleanField(default=False, help_text=b'Makes image take up full width of carousel. If set to true then height must be provided.')),
                ('width', models.PositiveIntegerField(default=0, help_text=b'Fixed width in pixels for carousel images. If left empty, width will be automatically calculated to preserve aspect ratio.', verbose_name=b'width')),
                ('height', models.PositiveIntegerField(default=0, help_text=b'Fixed height in pixels for carousel images. If left empty and width is given, height will be automatically calculated to preserve aspect ratio.', verbose_name=b'height')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='CarouselItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption_title', models.CharField(max_length=100, blank=True)),
                ('caption_content', models.TextField(blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'uploads/', blank=True)),
                ('url', models.CharField(default=None, max_length=256, blank=True)),
                ('carousel', models.ForeignKey(to='easy_carousel.Carousel')),
            ],
        ),
    ]
