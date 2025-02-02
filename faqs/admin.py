from django.contrib import admin
from .models import FAQ
from ckeditor.widgets import CKEditorWidget
from django import forms

class FAQAdminForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = '__all__'
        widgets = {
            'question': CKEditorWidget(),
            'answer': CKEditorWidget(),
            'question_hi': CKEditorWidget(),
            'question_bn': CKEditorWidget(),
            'answer_hi': CKEditorWidget(),
            'answer_bn': CKEditorWidget(),
        }

class FAQAdmin(admin.ModelAdmin):
    form = FAQAdminForm
    list_display = ('question', 'language')
    search_fields = ('question', 'answer', 'language')
    list_filter = ('language',)

admin.site.register(FAQ, FAQAdmin)
