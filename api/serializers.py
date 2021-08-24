from rest_framework import serializers
from .models import Teams, Team_Scores, Players, Games, Signed_contract, Player_Scores


#API 1
class PlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Players
        fields = ('url', 'player_name', 'player_team', 'id')

    def create(self, validated_data):
        name_verify = validated_data['player_name']
        if name_verify.isalnum() == False:
            raise serializers.ValidationError({'name': 'Player names can only contain letters and numbers.'})
        if name_verify[0].isnumeric() == True:
            raise serializers.ValidationError({'name': 'Player names cannot start with numbers.'})
        team_id = int(str(validated_data['player_team'])[14:-1])
        if len(Players.objects.filter(player_team=team_id)) <= 15:
            print(len(Players.objects.filter(player_team=team_id)))
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