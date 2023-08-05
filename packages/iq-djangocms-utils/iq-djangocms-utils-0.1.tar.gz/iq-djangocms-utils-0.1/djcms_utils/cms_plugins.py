# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import HiddenInput
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import CommonDataPluginModel

###############################################################################
class PluginHelpMixin(object):
    """
    provides a plugin help on the admin change_form.

    put a plugin_help before plugin class comment - thats all.
    """
    change_form_template = "admin/djcms_utils/plugins/plugin_change_form.html"

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if getattr(self, 'plugin_help', None):
            if not extra_context: extra_context = {}
            extra_context.update({
                'plugin_help': self.plugin_help.strip().replace('\n', '<br>')
            })
        return super(PluginHelpMixin, self).changeform_view(
                request, object_id, form_url, extra_context)

###############################################################################
class CommonDataPluginBase(CMSPluginBase):
    """
    Plugin Base for custom plugins, which use common data model.
    """
    model = CommonDataPluginModel
    name = _('Common Data')
    #form_extra_field_names = ['foo', 'bar'] must be definied in derived class

    def __init__(self, model=None, admin_site=None):
        super(CommonDataPluginBase, self).__init__(model, admin_site)

    def get_form(self, request, obj=None, **kwargs):
        f = super(CommonDataPluginBase, self).get_form(request, obj, **kwargs)
        f.base_fields['json_data'].widget = HiddenInput()
        if obj and obj.data:
            for k in self.form.base_fields.keys():
                # skip json_data which is our hidden obj data field
                if k == 'json_data': continue
                f.base_fields[k].initial = obj.data.get(k, None)
        return f

    def save_form(self, request, form, change):
        """ here we update our data (json_data) from extra_fields
        """
        obj = super(CommonDataPluginBase, self).save_form(request, form,
                change)
        data = {}
        for k in self.form.base_fields.keys():
            # skip json_data which is our hidden obj data field
            if k == 'json_data': continue
            data[k] = form.cleaned_data[k]
        obj.data = data
        return obj
