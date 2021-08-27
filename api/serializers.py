from rest_framework import serializers
from .models import Teams, Team_Scores, Players, Games, Signed_contract, Player_Scores


#API 1
class PlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Players
        fields = ('url', 'player_name', 'player_team', 'id')

    def create(self, validated_data):
        name_verify = validated_data['player_name']
        name_verify_no_spaces=name_verify.replace(' ','')
        if name_verify_no_spaces.isalnum() == False:
            raise serializers.ValidationError({'name': 'Player names can only contain letters and numbers.'})
        if name_verify_no_spaces[0].isnumeric() == True:
            raise serializers.ValidationError({'name': 'Player names cannot start with numbers.'})
        team_id = int(str(validated_data['player_team'])[14:-1])
        if len(Players.objects.filter(player_team=team_id)) <= 14:
            player = Players.objects.create(**validated_data)
            return player
        else:
            raise serializers.ValidationError({'name': 'Number of players in a team cannot exceeded 15.'})


#API 2
class GamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Games
        fields = ("id","game_date","team_1","team_2")

    def create(self, validated_data):
        team_1_selected = int(str(validated_data['team_1'])[14:-1])
        team_2_selected = int(str(validated_data['team_2'])[14:-1])
        # check if 1st team selected has games
        # check if 2nd team selected has games
        if team_1_selected != team_2_selected:
            if len(Games.objects.filter(team_1=team_1_selected, game_date=validated_data["game_date"])) == 0 and len(
                    Games.objects.filter(team_2=team_1_selected, game_date=validated_data["game_date"])) == 0:
                if len(Games.objects.filter(team_1=team_2_selected,
                                            game_date=validated_data["game_date"])) == 0 and len(
                    Games.objects.filter(team_2=team_2_selected, game_date=validated_data["game_date"])) == 0:
                    player = Games.objects.create(**validated_data)
                    return player
                else:
                    raise serializers.ValidationError(
                        {'name': f'Team {team_2_selected} already has a game on that day'})
            else:
                raise serializers.ValidationError({'name': f'Team {team_1_selected} already has a game on that day'})
        else:
            raise serializers.ValidationError({'name': 'The two teams selected are the same.'})


#API 4
class TeamsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teams
        fields = ("team_name", "id")


#API 5
class Signed_contractSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if len(Signed_contract.objects.filter(start_date_contract__gte=validated_data['start_date_contract'],
                                              end_date_contract__lte=validated_data['end_date_contract'])) == 0:
            contract = Signed_contract.objects.create(**validated_data)
            return contract
        else:
            player_id = int(str(validated_data['player_signed'])[16:-1])
            x = Players.objects.get(id=player_id)
            player = x.player_name
            raise serializers.ValidationError({'name': f'{player} has an active contract'})

    class Meta:
        model = Signed_contract
        fields = "__all__"


class PlayerScoresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player_Scores
        fields = ('id','game', 'player_scored', 'scored_points')


class TeamScoresSerializer(serializers.ModelSerializer):
    points = PlayerScoresSerializer(many=True, read_only=False, source='players_scores')

    class Meta:
        model = Team_Scores
        fields = ('id', 'scored_points', 'winner', 'game', 'team', "points")
