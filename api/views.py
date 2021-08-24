from django.http import HttpResponse,JsonResponse
from rest_framework import viewsets
from .models import Teams, Team_Scores, Players, Games, Signed_contract, Player_Scores
from api.serializers import PlayersSerializer, GamesSerializer, TeamsSerializer, Signed_contractSerializer
from django.db.models import Count, Q
from rest_framework.decorators import api_view
import numpy as np
from rest_framework import status
from rest_framework.response import Response
import os

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


# API 6
@api_view (['GET']) #puts in place API conventions - blocks methods other than get, changes the reques
#http://127.0.0.1:8000/home/?year=2022&player_id=1
def players_scores(request):
    if "year" not in request.query_params or "player_id" not in request.query_params:
        m="Please provide an year and a player id. Valid format example: .../players/?year=2021&player_id=1"
        return Response(m,status=status.HTTP_400_BAD_REQUEST)
    try:
        x = Player_Scores.objects.filter(game__game_date__year=request.query_params['year'], player_scored__id=request.query_params['player_id']).values_list(
            'game__game_date__month').annotate(total=Count('id'))
    except:
        m = f"Missing or Invalid Year or Player_id. Values entered - year:{request.query_params['year']} & player_id:{request.query_params['player_id']}." \
            f"  Example Format to use: .../players/?year=2021&player_id=1"
        # return JsonResponse(m, safe=False)
        return Response(m, status=status.HTTP_400_BAD_REQUEST)
    m="No results found"
    if x:
        z=np.array(x)
        y = z[:, 1]
        m=[int(i) for i in y]

        return JsonResponse(m, safe=False)
    return Response(m, status=status.HTTP_404_NOT_FOUND)