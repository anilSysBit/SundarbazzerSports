from typing import Any
from django.contrib import admin
from .models import TeamRequest,Team, PointTable, TieSheet, MatchStatus,RecentEvents,LatestNews,Player
from django.utils.html import mark_safe
# Register your models here.

@admin.register(TeamRequest)
class TeamRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_players','sports_genere','created_at')
    ordering = ('-created_at',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_players','sports_genere','created_at')

@admin.register(PointTable)
class PointTableAdmin(admin.ModelAdmin):
    list_display = ('team', 'points', 'status')
    # list_filter = ('status', 'team__name')
    # search_fields = ('team__name',)
    ordering = ('points','team')

@admin.register(TieSheet)
class TieSheetAdmin(admin.ModelAdmin):
    list_display = ('team1', 'team2', 'match_date', 'place','match_complete')
    # list_filter = ('match_date', 'place')
    # search_fields = ('team1__name', 'team2__name')
    exclude = ('match_complete',)

@admin.register(MatchStatus)
class MatchStatusAdmin(admin.ModelAdmin):
    list_display = ('game', 'team1_point', 'team2_point', 'winner')
    # list_filter = ('game__match_date', 'winner__name')
    # search_fields = ('game__team1__name', 'game__team2__name', 'winner__name')
    exclude = ('winner',)
    


# Recent Events Admin

@admin.register(RecentEvents)
class RecentEventsAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'event_title',
        'event_description',
        'sport_type',

    )

@admin.register(LatestNews)
class LatestNewsAdmin(admin.ModelAdmin):
    list_display = (
        'start_date',
        'end_date',
        'is_active',
        'image_preview',
        'sm_text'
    )
    def image_preview(self,obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100"/>')
        return "No Image"
    image_preview.short_description="Image"
    


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'jersey_no',
        'team',
        'age'
    )