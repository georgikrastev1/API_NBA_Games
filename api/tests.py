import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Teams, Team_Scores, Players, Games, Signed_contract, Player_Scores, Brands
from api.serializers import TeamsSerializer, PlayersSerializer, GamesSerializer, Signed_contractSerializer

client = APIClient()


# test API 1
class CreateNewPlayerTest(TestCase):

    def setUp(self):
        Teams.objects.create(team_name='API Test')
        Teams.objects.create(team_name='API Test 2')
        self.valid_payload = {
            'player_name': 'Muffin',
            'player_team': 2,
        }
        self.invalid_payload = {
            'player_name': '',
            'player_team': 2,
        }

    def test_create_valid_player(self):
        response = client.post(
            reverse('players-list'),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_player(self):
        response = client.post(
            reverse('players-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        response2 = client.post(
            reverse('players-list'),
            data=json.dumps({
                'player_name': '1asds',
                'player_team': 2,
            }),
            content_type='application/json'
        )
        response3 = client.post(
            reverse('players-list'),
            data=json.dumps({
                'player_name': '1*asds',
                'player_team': 2,
            }),
            content_type='application/json'
        )
        # Empty name
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Starts with number
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Contains non-alphanumeric characters
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_too_many_players(self):
        for i in range(1,17):
            response = client.post(
                reverse('players-list'),
                data=json.dumps({
                    'player_name': 'Georgi Krastev',
                    'player_team': 2,
                }),
                content_type='application/json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# Test API 2: Create Game

class CreateNewGameTest(TestCase):

    def setUp(self):
        Teams.objects.create(team_name='Team 1')
        Teams.objects.create(team_name='Team 2')
        Teams.objects.create(team_name='Team 3')
        self.valid_payload = {
            'game_date': '2021-08-20',
            'team_1': 1,
            'team_2': 2,
        }
        self.invalid_payload = {
            'game_date': '2021-08-20',
            'team_1': 1,
            'team_2': 2,
        }

    def test_create_valid_game(self):
        response = client.post(
            reverse('games-list'),
            data=json.dumps({
                'game_date': '2021-08-20',
                'team_1': 1,
                'team_2': 2,
            }),
            content_type='application/json'
        )
        response2 = client.post(
            reverse('games-list'),
            data=json.dumps({
                'game_date': '2021-08-21',
                'team_1': 1,
                'team_2': 2,
            }),
            content_type='application/json'
        )
        # Create a valid game
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Create a valid game with the same teams on a different date
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_game(self):
        response = client.post(
            reverse('games-list'),
            data=json.dumps({
                'game_date': '2021-08-20',
                'team_1': 1,
                'team_2': 2,
            }),
            content_type='application/json'
        )
        response2 = client.post(
            reverse('games-list'),
            data=json.dumps({
                'game_date': '2021-08-20',
                'team_1': 1,
                'team_2': 2,
            }),
            content_type='application/json'
        )
        response3 = client.post(
            reverse('games-list'),
            data=json.dumps({
                'game_date': '2021-08-22',
                'team_1': 1,
                'team_2': 1,
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Create a game with same teams on same date
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        # Create a game using the same id for both teams
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)


# API 3
class RecordscoresTest(TestCase):

    def setUp(self):
        Teams.objects.create(team_name='Team 1')
        Teams.objects.create(team_name='Team 2')
        Teams.objects.create(team_name='Team 3')
        Players.objects.create(player_name='Georgi', player_team_id=1)
        Players.objects.create(player_name='Umar', player_team_id=2)
        Players.objects.create(player_name='Roy', player_team_id=3)
        Games.objects.create(game_date="2021-08-20", team_1_id=1, team_2_id=2)
        Games.objects.create(game_date="2021-08-21", team_1_id=2, team_2_id=3)
        Games.objects.create(game_date="2021-08-22", team_1_id=1, team_2_id=3)

        self.valid_payload = {"items":
            [
                {
                    "game_id": 1,
                    "team_scores": [
                        {
                            "team_id": 1,
                            "points": 2
                        },
                        {
                            "team_id": 2,
                            "points": 3
                        }
                    ],
                    "player_scores": [
                        {
                            "player_id": 1,
                            "points": 2
                        },
                        {
                            "player_id": 2,
                            "points": 3
                        }
                    ]
                }
            ]
        }

        self.payload_game = {"items":
            [
                {
                    "game_id": 9,
                    "team_scores": [
                        {
                            "team_id": 1,
                            "points": 2
                        },
                        {
                            "team_id": 2,
                            "points": 3
                        }
                    ],
                    "player_scores": [
                        {
                            "player_id": 1,
                            "points": 2
                        },
                        {
                            "player_id": 2,
                            "points": 3
                        }
                    ]
                }
            ]
        }

        self.payload_teams = {"items":
            [
                {
                    "game_id": 1,
                    "team_scores": [
                        {
                            "team_id": 1,
                            "points": 2
                        },
                        {
                            "team_id": 1,
                            "points": 3
                        }
                    ],
                    "player_scores": [
                        {
                            "player_id": 1,
                            "points": 2
                        },
                        {
                            "player_id": 2,
                            "points": 3
                        }
                    ]
                }
            ]
        }

        self.payload_team_scores = {"items":
            [
                {
                    "game_id": 1,
                    "team_scores": [
                        {
                            "team_id": 1,
                            "points": 2
                        },
                        {
                            "team_id": 2,
                            "points": 2
                        }
                    ],
                    "player_scores": [
                        {
                            "player_id": 1,
                            "points": 2
                        },
                        {
                            "player_id": 2,
                            "points": 3
                        }
                    ]
                }
            ]
        }

        self.payload_team_not_in_game = {"items":
            [
                {
                    "game_id": 1,
                    "team_scores": [
                        {
                            "team_id": 1,
                            "points": 2
                        },
                        {
                            "team_id": 3,
                            "points": 2
                        }
                    ],
                    "player_scores": [
                        {
                            "player_id": 1,
                            "points": 2
                        },
                        {
                            "player_id": 2,
                            "points": 3
                        }
                    ]
                }
            ]
        }

        self.payload_player_duplicates = {"items":
            [
                {
                    "game_id": 1,
                    "team_scores": [
                        {
                            "team_id": 1,
                            "points": 2
                        },
                        {
                            "team_id": 2,
                            "points": 2
                        }
                    ],
                    "player_scores": [
                        {
                            "player_id": 1,
                            "points": 2
                        },
                        {
                            "player_id": 1,
                            "points": 3
                        }
                    ]
                }
            ]
        }

        self.payload_player_not_in_game = {"items":
            [
                {
                    "game_id": 1,
                    "team_scores": [
                        {
                            "team_id": 1,
                            "points": 2
                        },
                        {
                            "team_id": 2,
                            "points": 2
                        }
                    ],
                    "player_scores": [
                        {
                            "player_id": 1,
                            "points": 2
                        },
                        {
                            "player_id": 3,
                            "points": 3
                        }
                    ]
                }
            ]
        }
    def test_enter_valid_scores(self):
        url = reverse('teams_players_scores')
        data = self.valid_payload
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_enter_invalid_scores(self):
        url = reverse('teams_players_scores')
        # Invalid game id
        data = self.payload_game
        response1 = client.post(url, data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        # Same team ids
        data = self.payload_teams
        response2 = client.post(url, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        # Equal team scores
        data = self.payload_team_scores
        response3 = client.post(url, data, format='json')
        self.assertEqual(response3.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        #Teams not in game
        data = self.payload_team_not_in_game
        response4 = client.post(url, data, format='json')
        self.assertEqual(response4.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        # Players duplication
        data = self.payload_player_duplicates
        response5 = client.post(url, data, format='json')
        self.assertEqual(response5.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        # Players not in game
        data = self.payload_player_not_in_game
        response6 = client.post(url, data, format='json')
        self.assertEqual(response6.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

# API 4
class GetAllTeamsTest(TestCase):

    def setUp(self):
        Teams.objects.create(team_name='API Test')

    def test_get_all_teams(self):
        # get API response
        response = client.get(reverse('teams-list'))
        # get data from db
        teams_list = Teams.objects.all()
        serializer = TeamsSerializer(teams_list, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# API 5

class CreateNewContractTest(TestCase):

    def setUp(self):
        Teams.objects.create(team_name='Team 1')
        Teams.objects.create(team_name='Team 2')
        Teams.objects.create(team_name='Team 3')
        Players.objects.create(player_name='Georgi', player_team_id=1)
        Players.objects.create(player_name='Umar', player_team_id=2)
        Players.objects.create(player_name='Roy', player_team_id=3)
        Brands.objects.create(brand_name='Puma')
        Brands.objects.create(brand_name='Nike')
        Brands.objects.create(brand_name='Adidas')
        self.valid_payload = {
            'brand_signed_with': 1,
            'player_signed': 1,
            'start_date_contract': '2021-08-20',
            'end_date_contract': '2021-08-21',
        }
        self.invalid_payload = {
            'brand_signed_with': 1,
            'player_signed': 1,
            'start_date_contract': '2021-08-20',
            'end_date_contract': '2021-08-21',
        }

    def test_create_valid_contract(self):
        response = client.post(
            '/sign_contract/',
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_overlapping_contract(self):  # Same period
        response = client.post(
            '/sign_contract/',
            data=self.valid_payload
        )
        response2 = client.post(
            '/sign_contract/',
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)


# API 6

class ReturnPlayerScoresTest(TestCase):

    def setUp(self):
        Teams.objects.create(team_name='Team 1')
        Teams.objects.create(team_name='Team 2')
        Teams.objects.create(team_name='Team 3')
        Players.objects.create(player_name='Georgi', player_team_id=1)
        Players.objects.create(player_name='Alexander', player_team_id=1)
        Players.objects.create(player_name='Umar', player_team_id=2)
        Players.objects.create(player_name='Roy', player_team_id=3)
        Games.objects.create(game_date="2021-01-20", team_1_id=1, team_2_id=2)
        Games.objects.create(game_date="2021-02-21", team_1_id=1, team_2_id=3)
        Games.objects.create(game_date="2021-03-22", team_1_id=1, team_2_id=3)
        Games.objects.create(game_date="2021-04-22", team_1_id=1, team_2_id=3)
        Games.objects.create(game_date="2021-05-22", team_1_id=1, team_2_id=3)
        Games.objects.create(game_date="2021-06-22", team_1_id=1, team_2_id=3)
        Games.objects.create(game_date="2021-07-22", team_1_id=1, team_2_id=3)
        Games.objects.create(game_date="2021-08-22", team_1_id=1, team_2_id=3)
        Games.objects.create(game_date="2021-09-22", team_1_id=1, team_2_id=3)
        Games.objects.create(game_date="2021-10-22", team_1_id=1, team_2_id=3)
        Games.objects.create(game_date="2021-11-22", team_1_id=1, team_2_id=3)
        Games.objects.create(game_date="2021-12-22", team_1_id=1, team_2_id=3)
        Player_Scores.objects.create(game_id=1, player_scored_id=1, scored_points=19)
        Player_Scores.objects.create(game_id=1, player_scored_id=2, scored_points=100)
        Player_Scores.objects.create(game_id=2, player_scored_id=1, scored_points=20)
        Player_Scores.objects.create(game_id=3, player_scored_id=1, scored_points=20)
        Player_Scores.objects.create(game_id=4, player_scored_id=1, scored_points=20)
        Player_Scores.objects.create(game_id=5, player_scored_id=1, scored_points=20)
        Player_Scores.objects.create(game_id=6, player_scored_id=1, scored_points=20)
        Player_Scores.objects.create(game_id=7, player_scored_id=1, scored_points=20)
        Player_Scores.objects.create(game_id=8, player_scored_id=1, scored_points=20)
        Player_Scores.objects.create(game_id=9, player_scored_id=1, scored_points=20)
        Player_Scores.objects.create(game_id=10, player_scored_id=1, scored_points=20)
        Player_Scores.objects.create(game_id=11, player_scored_id=1, scored_points=20)
        Player_Scores.objects.create(game_id=12, player_scored_id=1, scored_points=21)
        Player_Scores.objects.create(game_id=12, player_scored_id=2, scored_points=100)

    def test_get_player_scores_valid(self):
        response = client.get(
            '/players/?year=2021&player_id=1',
        )
        self.assertEqual(len(response.data), 12)
        self.assertEqual(response.data, [19, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 21])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_player_scores_invalid(self):
        response = client.get(
            '/players/?year=&player_id=',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
