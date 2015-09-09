from django.db import models

from cms.models import CMSPlugin


class AccordionPlugin(CMSPlugin):
    name = models.CharField(
        max_length=80,
        help_text="The name for the accordion group.")
    use_glyphs = models.BooleanField(
        default=True,
        help_text="Whether or not to use arrows to indicate whether a group"
        " is closed or not.")


class Accordion(models.Model):
    accordion_group = models.ForeignKey(AccordionPlugin)
    title = models.CharField(max_length=255, blank=False)
    body = models.TextField(blank=False)
