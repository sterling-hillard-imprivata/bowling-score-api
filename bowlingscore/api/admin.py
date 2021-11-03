from django.contrib import admin

# Register your models here.
from .models import BowlingScore

class APIAdmin(admin.ModelAdmin):
  list = ('frame_num', 'pins', 'player', 'strike_spare', 'frame_score', 'total_score', 'tenth_frame_bonus_pins')

  readonly_fields=('frame_num', )

  admin.site.register(BowlingScore)