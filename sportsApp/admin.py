from typing import Any
from django.contrib import admin
from .models import TeamRequest,Team, PointTable,Coach, TieSheet, MatchStatus,RecentEvents,LatestNews,Player,Messages,Subscriber,Event,TeamStatus,PlayerStatus,Sponser
from django.utils.html import mark_safe
# Register your models here.

@admin.register(TeamRequest)
class TeamRequestAdmin(admin.ModelAdmin):
    list_display = ('registration_number','name', 'total_players','sports_genere','created_at')
    ordering = ('-created_at',)

class PlayerInline(admin.TabularInline):
    model = Player
    extra = 1

class CoachInline(admin.TabularInline):
    model = Coach
    extra = 1


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = [CoachInline,PlayerInline]
    list_display = ('name','logo_preview' ,'total_players','sports_genere','is_verified','created_at')
    readonly_fields = ('user',)
    def logo_preview(self,obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" width="50" height="50"/>')
        return "No Image"
    logo_preview.short_description="Image"
    

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
        'age',
        'image_preview',
        'designation'
    )
    def image_preview(self,obj):
        if obj.profile_image:
            return mark_safe(f'<img src="{obj.profile_image.url}" width="100" height="100"/>')
        return "No Image"
    image_preview.short_description="Image"

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "team",
        "image_preview"
    )



    def image_preview(self,obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100"/>')
        return "No Image"
    image_preview.short_description="Image"




@admin.register(TeamStatus)
class TeamStatusAdmin(admin.ModelAdmin):
    list_display = ('team', 'total_match_played', 'created_at')
    search_fields = ('team__name',)
    # list_filter = ('created_at',)

@admin.register(PlayerStatus)
class PlayerStatusAdmin(admin.ModelAdmin):
    list_display = ('player', 'total_match_played', 'total_goals', 'total_man_of_the_match')
    search_fields = ('player__name',)
    # list_filter = ('created_at',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_age_limit', 'is_verified', 'entry_fee', 'registration_start_date', 'resistration_end_date', 'event_start_date', 'event_end_date', 'created_at', 'updated_at')
    search_fields = ('title',)
    # list_filter = ('is_verified', 'registration_start_date', 'resistration_end_date', 'event_start_date', 'event_end_date', 'created_at', 'updated_at')

@admin.register(Sponser)
class SponserAdmin(admin.ModelAdmin):
    list_display = ('name', 'sponser_type', 'event', 'is_verified', 'created_at', 'updated_at')
    search_fields = ('name', 'event__title')
    # list_filter = ('sponser_type', 'is_verified', 'created_at', 'updated_at')

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)

@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('email', 'title', 'message', 'created_at')
    search_fields = ('email', 'title')