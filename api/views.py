from django.http import HttpResponse,JsonResponse
from rest_framework import viewsets
from .models import Teams, Team_Scores, Players, Games, Signed_contract, Player_Scores
from api.serializers import PlayersSerializer, GamesSerializer

#API 1
class PlayersViewSet(viewsets.ModelViewSet):
    queryset = Players.objects.all()
    serializer_class = PlayersSerializer


#API 2
class GamesViewSet(viewsets.ModelViewSet):
    queryset = Games.objects.all()
    serializer_class = GamesSerializer