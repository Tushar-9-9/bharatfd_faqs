from django.db import models
from django.core.cache import cache
from googletrans import Translator
from ckeditor.fields import RichTextField  # Ensure this is also imported


class FAQ(models.Model):
    question = models.TextField()  # Regular text for the main question
    answer = RichTextField()  # WYSIWYG editor for the answer (rich text)
    language = models.CharField(
        max_length=5, 
        choices=[('en', 'English'), ('hi', 'Hindi'), ('bn', 'Bengali')],
        default='en'  # Set a default language to avoid migration issues
    )
    question_hi = RichTextField(blank=True, default='')  # Treat this as rich text
    question_bn = RichTextField(blank=True, null=True)  # Allow null for Bengali translation of question

    def save(self, *args, **kwargs):
        # Translate question to other languages if not already provided
        if not self.question_hi:
            translator = Translator()
            # Translate to Hindi (hi) while preserving HTML tags
            self.question_hi = translator.translate(self.question, src='en', dest='hi').text
        
        if not self.question_bn:
            translator = Translator()
            # Translate to Bengali (bn) while preserving HTML tags
            self.question_bn = translator.translate(self.question, src='en', dest='bn').text
        
        super().save(*args, **kwargs)

    def get_translated_question(self, language_code='en'):
        cache_key = f"faq_question_{self.id}_{language_code}"
        translated_question = cache.get(cache_key)
        
        if not translated_question:
            # If no cached translation, use the appropriate translation
            if language_code == 'hi' and self.question_hi:
                translated_question = self.question_hi
            elif language_code == 'bn' and self.question_bn:
                translated_question = self.question_bn
            else:
                translated_question = self.question  # Default to the original question in English
            
            # Cache the translation for future requests
            cache.set(cache_key, translated_question, timeout=60*15)  # Cache for 15 minutes

        return translated_question
