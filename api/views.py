from django.http import HttpResponse,JsonResponse
from rest_framework import viewsets
from .models import Teams, Team_Scores, Players, Games, Signed_contract, Player_Scores
from api.serializers import PlayersSerializer, GamesSerializer, TeamsSerializer, Signed_contractSerializer
from django.db.models import Count, Q

#API 1
class PlayersViewSet(viewsets.ModelViewSet):
    queryset = Players.objects.all()
    serializer_class = PlayersSerializer


#API 2
class GamesViewSet(viewsets.ModelViewSet):
    queryset = Games.objects.all()
    serializer_class = GamesSerializer


#API 4
class TeamsViewSet(viewsets.ModelViewSet):
    queryset = Teams.objects.all().annotate(
        count_wins=Count('team_scores', filter=Q(team_scores__winner="Yes"))).order_by('-count_wins')
    serializer_class = TeamsSerializer


#API 5
class SignedContractViewSet(viewsets.ModelViewSet):
    queryset = Signed_contract.objects.all()
    serializer_class = Signed_contractSerializer