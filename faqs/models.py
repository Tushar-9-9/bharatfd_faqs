from django.db import models
from ckeditor.fields import RichTextField

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()  # This will enable WYSIWYG editor
    question_hi = models.TextField(blank=True, null=True)  # Hindi translation
    question_bn = models.TextField(blank=True, null=True)  # Bengali translation
    # You can add more languages as needed

    def __str__(self):
        return self.question

    def get_translated_text(self, language='en'):
        if language == 'hi' and self.question_hi:
            return self.question_hi
        if language == 'bn' and self.question_bn:
            return self.question_bn
        return self.question  # Fallback to the default question in English
