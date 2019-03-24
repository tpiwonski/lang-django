from rest_framework.views import APIView, Response

from dictionary.api.serializers import AddWordSerializer, WordSerializer, AddTranslationSerializer, TranslationSerializer, FindByWordSerializer, GetWordsSerializer
from dictionary.controllers import GetAllWords, AddWord, FindByWord, AddTranslation


class WordsAPIView(APIView):
    get_all_words_controller = GetAllWords()
    add_word_controller = AddWord()

    def get(self, request):
        words = self.get_all_words_controller.execute()

        data = GetWordsSerializer(words).data
        return Response(data={
            "data": data
        })

    def post(self, request):
        serializer = AddWordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        word = serializer.validated_data['word']
        language = serializer.validated_data['language']

        word = self.add_word_controller.execute(word=word, language=language)

        data = WordSerializer(word).data
        return Response(data={
            "data": data
        })


class WordAPIView(APIView):
    find_by_word_controller = FindByWord()

    def get(self, request, word):
        result = self.find_by_word_controller.execute(word=word)
        
        data = FindByWordSerializer(result).data
        return Response(data={
            "data": data
        })


class TranslationAPIView(APIView):
    add_translation_controller = AddTranslation()

    def post(self, request):
        serializer = AddTranslationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        source_word_id = serializer.validated_data['source_word_id']
        translated_word_id = serializer.validated_data['translated_word_id']

        translation = self.add_translation_controller.execute(source_word_id, translated_word_id)

        data = TranslationSerializer(translation).data
        return Response(data={
            "data": data
        })
