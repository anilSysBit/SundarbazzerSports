from typing import Any
from django.contrib import admin
from .models import TeamRequest,Team, PointTable,Coach,Goal,Fall,Substitution,PlayerMatchEvents, TieSheet, Match,MatchStatus,RecentEvents,LatestNews,Player,Messages,Subscriber,Event,TeamStatus,PlayerStatus,Sponser
from django.utils.html import mark_safe
from .utils import send_registration_mail
# Register your models here.

@admin.register(TeamRequest)
class TeamRequestAdmin(admin.ModelAdmin):
    list_display = ('registration_number','name', 'total_players','sports_genere','created_at')
    ordering = ('-created_at',)
    actions = ['send_registration_email_action']

    def send_registration_email_action(self,request,queryset):
        for team_request in queryset:
            email = team_request.email  # Assuming there's an email field in TeamRequest model
            registration_number = team_request.registration_number
            send_registration_mail(team_request.name,email, registration_number)
        self.message_user(request, "Emails sent successfully")
    send_registration_email_action.short_description = "Send registration email"

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


class GoalInline(admin.TabularInline):
    model = Goal
    extra = 1

class FallInline(admin.TabularInline):
    model = Fall
    extra = 1

class SubstitutionInline(admin.TabularInline):
    model = Substitution
    extra = 1

class PlayerEventsInline(admin.TabularInline):
    model = PlayerMatchEvents
    extra = 1

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    inlines = [GoalInline,FallInline,SubstitutionInline,PlayerEventsInline]
    list_display = ('team1','team2','match_date','place','match_complete')

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