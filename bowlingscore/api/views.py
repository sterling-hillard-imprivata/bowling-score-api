from django.shortcuts import render
from .models import Player, BowlingScore
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import PlayerSerializer,ScoreSerializer


# Create your views here.
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = BowlingScore.objects.all()
    serializer_class = ScoreSerializer
    template_name = "bowling_score.html"

    # @list_route(renderer_classes=[renderers.TemplateHTMLRenderer])
    # def blank_form(self, request, *args, **kwargs):
    #     serializer = ScoreSerializer()
    #     return Response({'serializer': serializer})

        