from django import forms
from .models import Document

# Model form for uploading files
class DocumentForm(forms.ModelForm):
  class Meta:
    model = Document
    fields = ('description', 'document', 'label')
