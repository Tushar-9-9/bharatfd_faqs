from django.contrib import admin
from .models import FAQ
from ckeditor.widgets import CKEditorWidget
from django import forms

class FAQAdmin(admin.ModelAdmin):
    form = forms.ModelForm
    list_display = ('question', 'language')
    search_fields = ('question', 'language')
    list_filter = ('language',)

    class Meta:
        model = FAQ

admin.site.register(FAQ, FAQAdmin)
