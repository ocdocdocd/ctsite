import re
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from easy_carousel.models import *
from django.utils.translation import ugettext as _
from django.contrib import admin
from django.forms import ModelForm, ValidationError


class CarouselForm(ModelForm):
    class Meta:
        model = Carousel
        exclude = []

    def clean_domid(self):
        data = self.cleaned_data['name']
        if not re.match(r'^[a-zA-Z_]\w*$', data):
            raise ValidationError(
                _("The name must be a single word beginning with a letter"))
        return data


class CarouselItemInline(admin.TabularInline):
    model = CarouselItem


class CMSCarouselPlugin(CMSPluginBase):
    model = Carousel
    form = CarouselForm
    module = _("Carousel")
    name = _("Carousel Plugin")
    render_template = "djangocms_carousel/carousel.html"

    inlines = [
        CarouselItemInline,
        ]

    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        return context

plugin_pool.register_plugin(CMSCarouselPlugin)
