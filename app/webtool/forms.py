from django import forms
from .models import Document
from .models import Hyperparameter

class DocumentForm(forms.ModelForm):
  class Meta:
    model = Document
    fields = ('description', 'document', 'label')

class HyperparameterForm(forms.ModelForm):
    class Meta:
        model = Hyperparameter
        fields = ('model_choice', 'hyperparameters', 'filename')
            
