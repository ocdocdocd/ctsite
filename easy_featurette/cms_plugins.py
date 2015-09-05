from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from easy_featurette.models import *
from django.utils.translation import ugettext as _
from django.contrib import admin
from django.forms import ModelForm


class FeaturetteForm(ModelForm):
    class Meta:
        model = FeaturettePlugin
        exclude = []


class FeaturetteInline(admin.TabularInline):
    model = Featurette


class CMSFeaturettePlugin(CMSPluginBase):
    model = FeaturettePlugin
    form = FeaturetteForm
    name = _("Featurette Plugin")
    render_template = 'djangocms_featurette/' + PLUGIN_TEMPLATES[0][0]

    inlines = [
        FeaturetteInline,
    ]

    def render(self, context, instance, placeholder):
        if instance and instance.template:
            self.render_template = 'djangocms_featurette/' + instance.template
        context.update({'instance': instance})
        return context

plugin_pool.register_plugin(CMSFeaturettePlugin)
