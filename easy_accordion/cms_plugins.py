from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from easy_accordion.models import *
from django.utils.translation import ugettext as _
from django.contrib import admin
from django.forms import ModelForm


class AccordionForm(ModelForm):
    class Meta:
        model = AccordionPlugin
        exclude = []


class AccordionInline(admin.TabularInline):
    model = Accordion


class CMSAccordionPlugin(CMSPluginBase):
    model = AccordionPlugin
    form = AccordionForm
    name = _("Accordion")
    render_template = 'djangocms_accordion/accordion.html'

    inlines = [
        AccordionInline,
    ]

    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        return context

plugin_pool.register_plugin(CMSAccordionPlugin)
