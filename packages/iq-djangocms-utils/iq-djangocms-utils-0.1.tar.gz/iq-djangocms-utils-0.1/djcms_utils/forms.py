# -*- coding: utf-8 -*-
from django import forms

from .models import CommonDataPluginModel
'''
class CustomAdminFormMetaClass(ModelFormMetaclass):
    """
    Metaclass for custom admin form with dynamic field
    """
    def __new__(cls, name, bases, attrs):
        for field in myloop: #add logic to get the fields
            attrs[field] = forms.CharField(max_length=30) #add logic to the form field
        return super(CustomAdminFormMetaClass, cls).__new__(cls, name, bases, attrs)


class CustomAdminForm(six.with_metaclass(CustomAdminFormMetaClass, forms.ModelForm)):
    """
'''

class CommonDataForm(forms.ModelForm):
    class Meta:
        model = CommonDataPluginModel
        fields = '__all__'
        """
        widgets = {
            'caption_text': forms.Textarea(attrs={'rows': 2}),
        }
        """
