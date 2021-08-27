from django.db import models

# Create your models here.
from django.db import models


class Teams(models.Model):
    team_name = models.CharField(max_length=100, null=False)

    class Meta:
        verbose_name_plural = 'Teams'


class Players(models.Model):
    player_name = models.CharField(max_length=100, null=False)
    player_team = models.ForeignKey(Teams, on_delete=models.CASCADE, )

    class Meta:
        verbose_name_plural = 'Players'


class Games(models.Model):
    game_date = models.DateField()
    team_1 = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='team_1')
    team_2 = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='team_2')

    class Meta:
        verbose_name_plural = 'Games'


class Team_Scores(models.Model):
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)
    scored_points = models.IntegerField()

    win_choice = (
        ('Yes', 'Yes',),
        ('No', 'No'),
    )

    winner = models.CharField(max_length=8, choices=win_choice, default='Yes')

    class Meta:
        verbose_name_plural = 'Team_Scores'

    def players_scores(self):
        return self.game.player_scores_set.all()


class Player_Scores(models.Model):
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    player_scored = models.ForeignKey(Players, on_delete=models.CASCADE)
    scored_points = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Player Scores'


class Brands(models.Model):
    brand_name = models.CharField(max_length=100, null=False)

    class Meta:
        verbose_name_plural = 'Brands'


class Signed_contract(models.Model):
    brand_signed_with = models.ForeignKey(Brands, on_delete=models.CASCADE)
    player_signed = models.ForeignKey(Players, on_delete=models.CASCADE, related_name='members')
    start_date_contract = models.DateField()
    end_date_contract = models.DateField()
