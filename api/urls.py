from django.urls import path, include
from api import views
from rest_framework import routers

router = routers.DefaultRouter()
#API 1
router.register('player', views.PlayersViewSet)
#API 2
router.register('game', views.GamesViewSet)
#API 4
router.register('teams', views.TeamsViewSet)
#API 5
router.register('sign-contract', views.SignedContractViewSet)

urlpatterns = [
    #API 6
    path('players/', views.players_scores, name="Players_Scores"),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]