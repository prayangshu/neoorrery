from django.contrib import admin
from .models import Planet, Comet, Asteroid

class PlanetAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'distance', 'semi_major_axis', 'eccentricity', 'last_updated')
    search_fields = ('name', 'nasa_id')
    list_filter = ('last_updated', 'eccentricity')
    readonly_fields = ('last_updated',)

class CometAdmin(admin.ModelAdmin):
    list_display = ('name', 'distance', 'orbital_period', 'eccentricity', 'last_updated')
    search_fields = ('name', 'nasa_id')
    list_filter = ('last_updated', 'eccentricity')
    readonly_fields = ('last_updated',)

class AsteroidAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'distance', 'is_potentially_hazardous', 'last_updated')
    search_fields = ('name', 'nasa_id')
    list_filter = ('is_potentially_hazardous', 'last_updated')
    readonly_fields = ('last_updated',)

admin.site.register(Planet, PlanetAdmin)
admin.site.register(Comet, CometAdmin)
admin.site.register(Asteroid, AsteroidAdmin)