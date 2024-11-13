from django.contrib import admin
from .models import Province, District, Municipality, Area

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'code')
    search_fields = ('name', 'province__name', 'code')
    list_filter = ('province',)

@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'code')
    search_fields = ('name', 'district__name', 'code')
    list_filter = ('district',)

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'municipality', 'code')
    search_fields = ('name', 'municipality__name', 'code')
    list_filter = ('municipality',)
