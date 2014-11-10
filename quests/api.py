

from .models import Quests
from .serializers import QuestSerializer


from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

class QuestsList(APIView):

    def get(self, request, format=None):
        quests = Quests.objects.all()
        serialized_quests = QuestSerializer(quests, many=True)
        return Response(serialized_quests.data)

class QuestsDetail(APIView):

    def get_object(self, pk):
        try:
            return Quests.objects.get(pk=pk)
        except Quests.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        quest = self.get_object(pk)
        serialized_quest = QuestSerializer(quest)
        return Response(serialized_quest.data)