from rest_framework.views import APIView, Response

from dictionary.controllers.word import GetAllWords, AddWord, FindWord, AddTranslation, WordInput, AddTranslationInput


class WordsView(APIView):
    get_all_words_controller = GetAllWords()
    add_word_controller = AddWord()

    def get(self, request):
        words = self.get_all_words_controller.execute()

        # data = WordsResponse(words).data
        return Response(data={
            'data': {
                'results': [
                    {'word': word} for word in words
                ]
            }
        })

    def post(self, request):
        serializer = WordInput(data=request.data)
        serializer.is_valid(raise_exception=True)

        word = serializer.validated_data['word']
        language = serializer.validated_data['language']

        word = self.add_word_controller.execute(word=word, language=language)

        # data = WordResultResponse(word).data
        return Response(data={
            'data': {
                'word': word
            }
        })


class WordView(APIView):
    find_word_controller = FindWord()

    def get(self, request, word):
        words = self.find_word_controller.execute(word=word)
        
        # data = WordsResponse(words).data
        return Response(data={
            'data': {
                'results': [
                    {'word': word} for word in words
                ]
            }
        })


# class TranslationAPIView(APIView):
#     add_translation_controller = AddTranslation()

#     def post(self, request):
#         serializer = AddTranslationSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         source_word_id = serializer.validated_data['source_word_id']
#         translated_word_id = serializer.validated_data['translated_word_id']

#         translation = self.add_translation_controller.execute(source_word_id, translated_word_id)

#         data = TranslationSerializer(translation).data
#         return Response(data={
#             "data": data
#         })

# class WordInput(Serializer):
#     word = CharField()
#     language = ChoiceField(choices=LANGUAGES)


# class TranslationRequest(Serializer):
#     word = CharField()
#     language = ChoiceField(choices=LANGUAGES)


# class AddTranslationRequest(Serializer):
#     word = WordRequest()
#     translations = TranslationRequest(many=True)


# class AddTranslationResponse(Serializer):
#     word_id = UUIDField()


class AddTranslationView(APIView):
    add_translation_controller = AddTranslation()

    def post(self, request):
        serializer = AddTranslationInput(data=request.data)
        serializer.is_valid(raise_exception=True)

        word = serializer.validated_data['word']
        translations = serializer.validated_data['translations']

        result = self.add_translation_controller.execute(word, translations)

        # data = WordResultResponse(result).data
        return Response(data={
            'data': {
                'word': result
            }
        })
