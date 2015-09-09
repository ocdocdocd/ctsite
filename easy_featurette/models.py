import os

from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile

from cms.models import CMSPlugin
from PIL import Image
from cStringIO import StringIO


PLUGIN_TEMPLATES = (
    ('left.html', 'Text on Left'),
    ('right.html', 'Text on Right'),
    ('alternating.html', "Alternating")
    )


class FeaturettePlugin(CMSPlugin):
    template = models.CharField('Template', max_length=255,
                                choices=PLUGIN_TEMPLATES)

    width = models.PositiveIntegerField(
        "Image Width",
        help_text="Fixed width in pixels for images."
        " If left empty and height is given, width will be automatically"
        " calculated to preserve aspect ratio.",
        default=0)

    height = models.PositiveIntegerField(
        "Image Height",
        help_text="Fixed height in pixels for images."
        " If left empty and width is given, width will be automatically"
        " calculated to preserve aspect ratio.",
        default=0)


class Featurette(models.Model):
    featurette = models.ForeignKey(FeaturettePlugin)
    heading = models.CharField(max_length=255, blank=False)
    muted_heading = models.CharField(max_length=255, blank=True)
    lead_text = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image.file)
            if img.mode not in ('L', 'RGB'):
                img = img.convert('RGB')

            if (self.featurette.width > 0 or self.featurette.height > 0):
                if self.featurette.width > 0 and self.featurette.height <= 0:
                    x = self.featurette.width
                    ratio = self.featurette.width / float(img.size[0])
                    y = int(ratio * img.size[1])
                elif self.featurette.height > 0 and self.featurette.width <= 0:
                    y = self.featurette.height
                    ratio = self.featurette.height / float(img.size[1])
                    x = int(ratio * img.size[0])
                else:
                    x = self.featurette.width
                    y = self.featurette.height
                img = img.resize((x, y), Image.ANTIALIAS)

                ext = os.path.splitext(self.image.name)[-1][1:]
                img_format = ext
                if img_format.lower() == 'jpg':
                    img_format = 'JPEG'

                temp_handle = StringIO()
                img.save(temp_handle, img_format)
                temp_handle.seek(0)

                con_type = 'image/%s' % ext

                suf = SimpleUploadedFile(ext,
                                         temp_handle.read(),
                                         content_type=con_type)
                fname = "%s.%s" % (os.path.splitext(self.image.name)[0], ext)
                self.image.save(fname, suf, save=False)

        super(Featurette, self).save()
