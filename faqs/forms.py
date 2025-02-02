from django import forms
from .models import FAQ
from ckeditor.widgets import CKEditorWidget

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'language']

    answer = forms.CharField(widget=CKEditorWidget())  # WYSIWYG editor for the answer
