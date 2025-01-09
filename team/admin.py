from django.contrib import admin
from .models import TeamOwner, Team,PointTable,Coach,Player,TeamDesign,TeamStatus
from django.utils.html import mark_safe

# Register your models here.
class PlayerInline(admin.StackedInline):
    model = Player
    extra = 1

class CoachInline(admin.StackedInline):
    model = Coach
    extra = 1

class TeamDesignInline(admin.StackedInline):
    model = TeamDesign
class TeamOwnerInline(admin.StackedInline):
    model = TeamOwner

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = [TeamOwnerInline,TeamDesignInline,CoachInline]
    list_display = ('id','name','logo_preview','email' ,'phone','total_players','sports_genere','is_verified','created_at')
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



@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "team",
        # "image_preview",
    )



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
    list_filter = ('team',)
    
    def image_preview(self,obj):
        if obj.profile_image:
            return mark_safe(f'<img src="{obj.profile_image.url}" width="100" height="100"/>')
        return "No Image"
    image_preview.short_description="Image"




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


