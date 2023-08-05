# -*- coding: utf-8 -*-
from django.db import models

from cms.models.pluginmodel import CMSPlugin

from dj_utils.models import TimeStampedDataModel

class CommonData(TimeStampedDataModel):
    """
    # common data can be saved as json with an data_type key.
    """
    data_type = models.CharField(max_length=100)

    def __str__(self):
        return self.data_type

class CommonDataPluginModel(CMSPlugin, TimeStampedDataModel):

    @property
    def label(self):
        return self.data.get('label', '')

    def get_short_description(self):
        ''' you may put a label field into the form to give the plugin a label
        for the cms structure view
        '''
        if self.label:
            return self.label
        else:
            return super(CommonDataPluginModel, self).get_short_description()
