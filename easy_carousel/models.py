import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models

from cms.models import CMSPlugin
from PIL import Image
from cStringIO import StringIO


class Carousel(CMSPlugin):
    name = models.CharField(max_length=50, verbose_name='Name')

    interval = models.IntegerField(
        default=5000,
        help_text="The amount of time in milliseconds to delay"
        " cycling items. If zero, carousel will not auto-cycle.")

    show_title = models.BooleanField(
        help_text="Display image titles, if true.",
        default=False)

    show_caption = models.BooleanField(
        help_text="Display caption text, if true.",
        default=False)

    show_controls = models.BooleanField(
        help_text="Display carousel controls, if true.",
        default=False)

    show_indicator = models.BooleanField(
        help_text="Display slide indicator, if true.",
        default=False)

    width = models.PositiveIntegerField(
        "width",
        help_text="Fixed width in pixels for carousel images."
        " If left empty and height is given, width will be automatically"
        " calculated to preserve aspect ratio.",
        default=0)

    height = models.PositiveIntegerField(
        "height",
        help_text="Fixed height in pixels for carousel images."
        " If left empty and width is given, height will be automatically"
        " calculated to preserve aspect ratio.",
        default=0)

    def size(self):
        return (self.width, self.height)

    def copy_relations(self, oldinstance):
        for item in oldinstance.carouselitem_set.all():
            item.pk = None
            item.carousel = self
            item.save()

    def __unicode__(self):
        return self.name


class CarouselItem(models.Model):
    carousel = models.ForeignKey(Carousel)
    caption_title = models.CharField(max_length=100, blank=True)
    caption_content = models.TextField(blank=True)
    image = models.ImageField(upload_to="uploads/", blank=True, null=True)
    url = models.CharField(max_length=256, blank=True, default=None)

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image.file)
            if img.mode not in ('L', 'RGB'):
                img = img.convert('RGB')

            if (self.carousel.width > 0 or self.carousel.height > 0):
                if self.carousel.width > 0 and self.carousel.height <= 0:
                    x = self.carousel.width
                    ratio = self.carousel.width / float(img.size[0])
                    y = int(ratio * img.size[1])
                elif self.carousel.height > 0 and self.carousel.width <= 0:
                    y = self.carousel.height
                    ratio = self.carousel.height / float(img.size[1])
                    x = int(ratio * img.size[0])
                else:
                    x, y = self.carousel.size()
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

        super(CarouselItem, self).save()
