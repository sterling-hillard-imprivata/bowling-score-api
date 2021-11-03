from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('bowling', ScoreViewSet, basename = 'bowling')
router.register('players', PlayerViewSet, basename = 'players')


urlpatterns = [
    path('api/', include(router.urls), name = 'api')
]