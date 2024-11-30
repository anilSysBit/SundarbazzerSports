from django.contrib import admin
from .models import Guest,Goal,Fall,Substitution,PlayerMatchEvents, Match,MatchTimeManager

# Register your models here.



class GoalInline(admin.TabularInline):
    model = Goal
    extra = 1

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    
    list_display = ('id','player','match','goal_time','goal_type')

@admin.register(Fall)
class FoulAdmin(admin.ModelAdmin):
    list_display = ('id','player','match','fall_time','fall_type','fall_category')


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
    list_display = ('team_vs','match_date','place','match_complete')


    def team_vs(self,obj):
        return f'{obj.team1} vs {obj.team2}'


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name','designation','is_event_guest','match')


@admin.register(MatchTimeManager)
class MatchTimeManagerAdmin(admin.ModelAdmin):
    list_display = ('match', 'start_time', 'resumed_time', 'paused_time', 'total_elapsed_time', 'extra_time')
    list_filter = ('start_time', 'resumed_time')
    search_fields = ('match__id',)
    readonly_fields = ('total_elapsed_time',)
    fieldsets = (
        (None, {
            'fields': ('match', 'start_time', 'resumed_time', 'paused_time', 'half_time_interval', 'extra_time', 'full_time_duration', 'total_elapsed_time')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (),
        }),
    )