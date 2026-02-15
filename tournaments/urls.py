from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TournamentViewSet, GroupViewSet, MatchViewSet,
    StandingsViewSet, FinalStageViewSet, FinalStageMatchViewSet
)

app_name = 'tournaments'

router = DefaultRouter()
router.register(r'tournaments', TournamentViewSet, basename='tournament')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'matches', MatchViewSet, basename='match')
router.register(r'standings', StandingsViewSet, basename='standing')
router.register(r'final-stages', FinalStageViewSet, basename='final-stage')
router.register(r'final-matches', FinalStageMatchViewSet, basename='final-match')

urlpatterns = [
    path('', include(router.urls)),
]
