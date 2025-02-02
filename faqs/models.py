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
    question_hi = RichTextField(blank=True, default='')  # Hindi translation (rich text)
    question_bn = RichTextField(blank=True, null=True)  # Bengali translation (rich text)
    answer_hi = RichTextField(blank=True, default='')  # Hindi translation (rich text)
    answer_bn = RichTextField(blank=True, null=True)  # Bengali translation (rich text)

    def save(self, *args, **kwargs):
        translator = Translator()  # Instantiate once for reuse

        if not self.question_hi:
            self.question_hi = translator.translate(self.question, src='en', dest='hi').text
        if not self.question_bn:
            self.question_bn = translator.translate(self.question, src='en', dest='bn').text

        if not self.answer_hi:
            self.answer_hi = translator.translate(self.answer, src='en', dest='hi').text
        if not self.answer_bn:
            self.answer_bn = translator.translate(self.answer, src='en', dest='bn').text

        super().save(*args, **kwargs)
        self.update_cache()

    def update_cache(self):
        """
        Updates the cache with the latest translations after saving.
        """
        cache.set(f"faq_question_{self.id}_hi", self.question_hi, timeout=60*15)
        cache.set(f"faq_question_{self.id}_bn", self.question_bn, timeout=60*15)
        cache.set(f"faq_question_{self.id}_en", self.question, timeout=60*15)
        cache.set(f"faq_answer_{self.id}_hi", self.answer_hi, timeout=60*15)
        cache.set(f"faq_answer_{self.id}_bn", self.answer_bn, timeout=60*15)
        cache.set(f"faq_answer_{self.id}_en", self.answer, timeout=60*15)

    def get_translated_content(self, language_code='en'):
        """
        Fetch the translated question and answer, either from cache or database.
        """
        question_cache_key = f"faq_question_{self.id}_{language_code}"
        answer_cache_key = f"faq_answer_{self.id}_{language_code}"

        translated_question = cache.get(question_cache_key)
        translated_answer = cache.get(answer_cache_key)

        if not translated_question:
            translated_question = getattr(self, f'question_{language_code}', self.question)
            cache.set(question_cache_key, translated_question, timeout=60*15)
        
        if not translated_answer:
            translated_answer = getattr(self, f'answer_{language_code}', self.answer)
            cache.set(answer_cache_key, translated_answer, timeout=60*15)

        return translated_question, translated_answer
