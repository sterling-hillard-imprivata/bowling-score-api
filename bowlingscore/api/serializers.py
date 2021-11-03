from rest_framework import serializers
from .models import Player, BowlingScore


class PlayerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Player
        fields = ['id', 'name', 'game']

class ScoreSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(read_only=True, slug_field = 'name')
    class Meta:
        model = BowlingScore
        fields = ['id', 'frame_num', 'first_roll', 'second_roll','player','name', 'strike_spare', 'tenth_frame_bonus_pins', 'frame_score', 'total_score']
        

