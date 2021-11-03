from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from .constants import *

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length = 50)
    game = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ["name", "game"]

class BowlingScore(models.Model):
    frame_num = models.IntegerField(validators=[
                                        MinValueValidator(1),
                                        MaxValueValidator(10)])
    first_roll = models.IntegerField(validators=[
                                        MinValueValidator(0),
                                        MaxValueValidator(10)])
    second_roll = models.IntegerField(validators=[
                                        MinValueValidator(0),
                                        MaxValueValidator(10)])
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tenth_frame_bonus_pins = models.IntegerField(validators=[
                                        MinValueValidator(0),
                                        MaxValueValidator(20)], default=0)

    class Meta:
        unique_together = ["frame_num", "player"]
    

    @property
    def strike_spare(self):
        # If the first roll knocks out 10 its a strike
        if self.first_roll == 10:
            return 'strike'
        # Any combination of rolls resulting in greater than 10 pins that's not a strike is a spare
        if self.first_roll + self.second_roll >= 10:
            return 'spare'
        else:
            return 'neither'
    @property
    def pins(self):
        if self.first_roll + self.second_roll < 10:
            return self.first_roll + self.second_roll
        else:
            # Don't allow user input to be greater than 10
            return 10
        
    @property
    def frame_score(self):
            q1 = BowlingScore.objects.get(frame_num = self.frame_num, player = self.player)
            if q1.strike_spare == 'neither':
                return q1.pins
            #any frame that's a strike looks for the pins in the next two succeeding frames
            if q1.strike_spare == 'strike':
                try:
                    q2 = BowlingScore.objects.get(frame_num = self.frame_num + 1, player = self.player)
                    q3 = BowlingScore.objects.get(frame_num = self.frame_num + 2, player = self.player)
                    return q1.pins + q2.pins + q3.pins
                except BowlingScore.DoesNotExist:
                    pass
            # frames that are strikes and spares begin to add the pins in the next frame. Strikes will be overwritten
            #  by the logic above if there are two succeeding frames.
            if q1.strike_spare in ['spare','strike']:
                try: 
                    q2 = BowlingScore.objects.get(frame_num = self.frame_num + 1, player = self.player)
                    return q1.pins + q2.pins
                except BowlingScore.DoesNotExist:
                    pass
            if self.frame_num <10:
                return self.pins
            # if the tenth frame results in a strike or spare, the player may add the bonus pins field to there score in the end
            if self.frame_num == 10 and self.strike_spare in ['strike', 'spare']:
                return self.pins + self.tenth_frame_bonus_pins

    @property
    def total_score(self):
        if self.frame_num > 1:
            previous_frame = self.frame_num - 1
            # Looks at the perceding frame's total score and adds the that score to the current frame score.
            try:
                query = BowlingScore.objects.get(frame_num = previous_frame, player = self.player)
                self.previous_total = query.total_score
                return self.frame_score + self.previous_total
            # If for any reason there is no record of the previous frame, the current frame score is returned
            except BowlingScore.DoesNotExist:
                return self.frame_score
        else: 
            return self.frame_score
