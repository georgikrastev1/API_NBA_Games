from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from .models import Teams, Team_Scores, Players, Games, Signed_contract, Player_Scores
from api.serializers import PlayersSerializer, GamesSerializer, TeamsSerializer, Signed_contractSerializer, \
    TeamScoresSerializer
from django.db.models import Count, Q, Sum
from rest_framework.decorators import api_view
import numpy as np
from rest_framework import status
from rest_framework.response import Response
import os
import time, timeit


# API 1
class PlayersViewSet(viewsets.ModelViewSet):
    queryset = Players.objects.all()
    serializer_class = PlayersSerializer


# API 2
class GamesViewSet(viewsets.ModelViewSet):
    queryset = Games.objects.all()
    serializer_class = GamesSerializer


# API 3
@api_view(['POST'])
def teams_players_scores(request):
    scores_all = request.data.get("items")

    # check if Games id is provided and if game exists
    try:
        game_id = scores_all[0].get("game_id")
        game_get = Games.objects.get(pk=game_id)
    except:
        m = f"Invalid game id."
        return Response(m, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    team_information = scores_all[0].get("team_scores")
    team_members = []

    # Check if game score has already been recorded
    if Team_Scores.objects.filter(game_id=game_id):
        m = f"Results for the game have already been entered."
        return Response(m, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # Check if  two teams are submitted
    if len(team_information) != 2:
        m = f"Exactly 2 teams have to be submitted."
        return Response(m, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # Check if teams submitted are different
    team_1_id=team_information[0].get("team_id")
    team_2_id = team_information[1].get("team_id")

    if type(team_1_id)!=int or type(team_2_id)!=int:
        m = f"Invalid data format"
        return Response(m, status=status.HTTP_400_BAD_REQUEST)
    if team_1_id == team_2_id:
        m = f"Team ids are the same."
        return Response(m, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    #Check if teams really exist:
    try:
        team_get = Teams.objects.get(pk=team_1_id)
        team_players = Players.objects.filter(player_team=team_get).values_list('id', flat=True)
        team_members.extend(team_players)  # to be used to check if players are part of the tams
        # Check if team really played in the game
        if game_get.team_1_id != team_get.pk and game_get.team_2_id != team_get.pk:
            m = f"Team {team_get.pk} did not participate in this game."
            return Response(m, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except:
        m = f"Please provide a valid team. ID of first team entered is invalid."
        return Response(m, status=status.HTTP_400_BAD_REQUEST)

    try:
        team_get = Teams.objects.get(pk=team_2_id)
        team_players = Players.objects.filter(player_team=team_get).values_list('id', flat=True)
        team_members.extend(team_players)  # to be used to check if players are part of the teams
        # Check if team really played in the game
        if game_get.team_1_id != team_get.pk and game_get.team_2_id != team_get.pk:
            m = f"Team {team_get.pk} did not participate in this game."
            return Response(m, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except:
        m = f"Please provide a valid team. ID of second team entered is invalid."
        return Response(m, status=status.HTTP_400_BAD_REQUEST)

    # Check that there is a definite winner and assign winner
    team_1_points=team_information[0].get("points")
    team_2_points = team_information[1].get("points")
    if type(team_1_points)!=int or type(team_2_points)!=int:
        m = f"Invalid data format"
        return Response(m, status=status.HTTP_400_BAD_REQUEST)
    if team_1_points == team_2_points:
        m = f"The two teams cannot have equal scores. There must be a winner."
        return Response(m, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    win_team_1="No"
    win_team_2 = "Yes"
    if team_information[0].get("points")>team_information[1].get("team_id"):
        win_team_1="Yes"
        win_team_2 = "No"

    # check if there are player duplicates:
    scores_players = scores_all[0].get("player_scores")
    player_ids=[]
    for i in scores_players:
        player_id = i.get("player_id")
        if type(player_id) != int:
            m = f"Invalid data format for player {player_id}'s id "
            return Response(m, status=status.HTTP_400_BAD_REQUEST)
        player_ids.append(player_id)
        points=i.get("points")
        if type(points) != int:
            m = f"Invalid data format for player {player_id}'s points "
            return Response(m, status=status.HTTP_400_BAD_REQUEST)
    if len(player_ids) != len(set(player_ids)):
        m = f"There are duplicate player ids."
        return Response(m, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # Check if all players submitted really play in that team
    for player in player_ids:
        if player not in team_members:
            m = f"Player {player} is not part of any of the two teams."
            return Response(m, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


    if type(team_1_points) != int or type(team_2_points) != int:
        m = f"Invalid data format"
        return Response(m, status=status.HTTP_400_BAD_REQUEST)

    # Save team score

    save_team_1_score = Team_Scores(game=game_get, team_id=team_information[0].get("team_id"),
                                    scored_points=team_information[0].get("points"),
                                    winner=win_team_1)
    save_team_1_score.save()

    save_team_2_score = Team_Scores(game=game_get, team_id=team_information[1].get("team_id"),
                                    scored_points=team_information[1].get("points"),
                                    winner=win_team_2)
    save_team_2_score.save()

    # Save Players scores
    players_sum_points_check = 0
    for i in range(0, len(scores_players)):
        save_player_score = Player_Scores(game=game_get, player_scored_id=scores_players[i].get("player_id"),
                                          scored_points=scores_players[i].get('points'))
        save_player_score.save()
        players_sum_points_check = players_sum_points_check+scores_players[i].get('points')

    # check if sum of players' scores are equal to the team's score
    team_sum_scores=team_information[0].get("points")+team_information[1].get("points")
    if players_sum_points_check != team_sum_scores:
        m = f"Successfully Created. Please be aware that the sum of the players'scores ({players_sum_points_check}) is not equal to the total points of the team ({team_sum_scores})"
        return Response(m, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_201_CREATED)


# API 4
class TeamsViewSet(viewsets.ModelViewSet):
    queryset = Teams.objects.all().annotate(
        count_wins=Count('team_scores', filter=Q(team_scores__winner="Yes"))).order_by('-count_wins')
    serializer_class = TeamsSerializer


# API 5
class SignedContractViewSet(viewsets.ModelViewSet):
    queryset = Signed_contract.objects.all()
    serializer_class = Signed_contractSerializer


# API 6
@api_view(['GET'])  # puts in place API conventions - blocks methods other than get, changes the reques
# http://127.0.0.1:8000/players/?year=2021&player_id=41
def players_scores(request):
    if "year" not in request.query_params or "player_id" not in request.query_params:
        m = "Please provide an year and a player id. Valid format example: .../players/?year=2021&player_id=1"
        return Response(m, status=status.HTTP_400_BAD_REQUEST)
    try:
        x = Player_Scores.objects.filter(game__game_date__year=request.query_params['year'],
                                         player_scored__id=request.query_params['player_id']).values_list(
            'game__game_date__month').annotate(total=Sum('scored_points'))
    except:
        m = f"Missing or Invalid Year or Player_id. Values entered - year:{request.query_params['year']} & player_id:{request.query_params['player_id']}." \
            f"  Example Format to use: .../players/?year=2021&player_id=1"
        # return JsonResponse(m, safe=False)
        return Response(m, status=status.HTTP_400_BAD_REQUEST)
    m = "No results found"
    if x:
        z = np.array(x)
        month_all=[[x,0] for x in range(1,13)]
        for x in z:
            for i in month_all:
                if x[0]==i[0]:
                    i[1]=x[1]
        m=[x[1] for x in month_all]
        return Response(m)
    return Response(m, status=status.HTTP_404_NOT_FOUND)


class TeamScoresViewSet(viewsets.ModelViewSet):
    queryset = Team_Scores.objects.all()
    serializer_class = TeamScoresSerializer
