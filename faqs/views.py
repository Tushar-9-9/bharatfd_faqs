from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import FAQ
from .serializers import FAQSerializer
from django.core.cache import cache

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    @action(detail=True, methods=['get'], url_path='translate')
    def translate(self, request, pk=None):
        """
        Custom action to fetch translated FAQ based on the lang parameter.
        Example: /api/faqs/<pk>/translate/?lang=hi
        """
        faq = self.get_object()
        language_code = request.query_params.get('lang', 'en')  # Default to English
        translated_question, translated_answer = faq.get_translated_content(language_code)
        
        # Cache key for both translated question and answer
        cache_key = f"faq_{faq.id}_{language_code}"
        cached_translation = cache.get(cache_key)

        if not cached_translation:
            cached_translation = {
                "translated_question": translated_question,
                "translated_answer": translated_answer
            }
            cache.set(cache_key, cached_translation, timeout=60*15)  # Cache for 15 minutes

        return Response(cached_translation)
