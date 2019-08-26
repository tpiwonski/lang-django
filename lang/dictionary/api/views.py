from rest_framework.views import APIView, Response

from lang.dictionary.controllers.add_entry import AddEntry
from lang.dictionary.controllers.get_all_entries import GetAllEntries
from lang.dictionary.controllers.get_entry import GetEntry
from lang.dictionary.controllers.search_entries import SearchEntries
from lang.dictionary.serializers import EntryInput, AddTranslationInput


class EntriesView(APIView):
    get_all_entries_controller = GetAllEntries()
    add_entry_controller = AddEntry()

    def get(self, request):
        entries = self.get_all_entries_controller.execute()

        return Response(data={
            'data': {
                'results': [
                    {'entry': entry} for entry in entries
                ]
            }
        })

    def post(self, request):
        serializer = EntryInput(data=request.data)
        serializer.is_valid(raise_exception=True)

        text = serializer.validated_data['text']
        language = serializer.validated_data['language']

        entry = self.add_entry_controller.execute(text=text, language=language)

        return Response(data={
            'data': {
                'entry': entry
            }
        })


class EntryView(APIView):
    get_entry_controller = GetEntry()

    def get(self, request, entry_id):
        entry = self.get_entry_controller.execute(entry_id)
        return Response(data={
            'data': {
                'entry': entry
            }
        })


class SearchEntryView(APIView):
    find_entry_controller = SearchEntries()

    def get(self, request, text):
        entries = self.find_entry_controller.execute(text=text)
        
        # data = WordsResponse(words).data
        return Response(data={
            'data': {
                'results': [
                    {'entry': entry} for entry in entries
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


class TranslationsView(APIView):
    add_translation_controller = AddEntry()

    def post(self, request):
        serializer = AddTranslationInput(data=request.data)
        serializer.is_valid(raise_exception=True)

        entry = serializer.validated_data['entry']
        translations = serializer.validated_data['translations']

        result = self.add_translation_controller.execute(entry, translations)

        # data = WordResultResponse(result).data
        return Response(data={
            'data': {
                'entry': result
            }
        })
