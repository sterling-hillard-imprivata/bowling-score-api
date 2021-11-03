from rest_framework import serializers
from .models import Player, BowlingScore


class PlayerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Player
        fields = ['id', 'name', 'game']

class ScoreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BowlingScore
        fields = ['id', 'frame_num', 'first_roll', 'second_roll','player', 'strike_spare', 'tenth_frame_bonus_pins', 'frame_score', 'total_score']
        

