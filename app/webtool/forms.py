"""
This module details the structure of all the forms the webtool uses. The schemas will eventually be
translated into HTML in the templates
"""

from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    """
    Model form for uploading files
    """
    class Meta:
        """
        meta info for Django Model Forms
        """
        model = Document
        fields = ('description', 'document', 'label')
