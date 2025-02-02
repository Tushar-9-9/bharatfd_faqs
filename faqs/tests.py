from django.test import TestCase
from faqs.models import FAQ
from googletrans import Translator


class FAQModelTest(TestCase):

    def test_translation(self):
        # Create an FAQ object
        faq = FAQ.objects.create(
            question='What is Django?',
            answer='Django is a high-level Python web framework.',
        )
        faq.save()

        # Check if question_hi is translated (Hindi)
        self.assertTrue(faq.question_hi)
        expected_hi_translation = Translator().translate('What is Django?', src='en', dest='hi').text
        self.assertEqual(faq.question_hi, expected_hi_translation)

        # Check if question_bn is translated (Bengali)
        self.assertTrue(faq.question_bn)
        expected_bn_translation = Translator().translate('What is Django?', src='en', dest='bn').text
        self.assertEqual(faq.question_bn, expected_bn_translation)

    def test_get_translated_question(self):
        # Create FAQ objects for multiple languages
        faq = FAQ.objects.create(
            question='What is Django?',
            answer='Django is a high-level Python web framework.',
        )
        faq.save()

        # Check if get_translated_question method works for Hindi
        translated_question_hi = faq.get_translated_question(language_code='hi')
        self.assertEqual(translated_question_hi, faq.question_hi)

        # Check if get_translated_question method works for Bengali
        translated_question_bn = faq.get_translated_question(language_code='bn')
        self.assertEqual(translated_question_bn, faq.question_bn)
