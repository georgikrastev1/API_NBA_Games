from django.urls import path, include
from api import views
from rest_framework import routers

router = routers.DefaultRouter()
#API 1
router.register('player', views.PlayersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]