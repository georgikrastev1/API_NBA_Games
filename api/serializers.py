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



