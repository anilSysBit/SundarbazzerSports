from typing import Any
from django.contrib import admin
from .models import Team, PointTable, TieSheet, MatchStatus

# Register your models here.

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_code', 'total_players', 'total_match_played')
    # search_fields = ('name', 'team_code')
    

@admin.register(PointTable)
class PointTableAdmin(admin.ModelAdmin):
    list_display = ('team', 'points', 'status')
    # list_filter = ('status', 'team__name')
    # search_fields = ('team__name',)
    ordering = ('points','team')

@admin.register(TieSheet)
class TieSheetAdmin(admin.ModelAdmin):
    list_display = ('team1', 'team2', 'match_date', 'place')
    # list_filter = ('match_date', 'place')
    # search_fields = ('team1__name', 'team2__name')

@admin.register(MatchStatus)
class MatchStatusAdmin(admin.ModelAdmin):
    list_display = ('game', 'team1_point', 'team2_point', 'winner')
    # list_filter = ('game__match_date', 'winner__name')
    # search_fields = ('game__team1__name', 'game__team2__name', 'winner__name')
    exclude = ('winner',)
    