from django.contrib import admin
from .models import Planet, Comet, Asteroid, CelestialBodyStats, UserProfile, BlogPost, Topic

# Admin configuration for Planet
class PlanetAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'distance', 'semi_major_axis', 'eccentricity', 'last_updated')
    search_fields = ('name', 'nasa_id')
    list_filter = ('last_updated', 'eccentricity')
    readonly_fields = ('last_updated',)
    fieldsets = (
        ('General Information', {
            'fields': ('name', 'nasa_id', 'last_updated')
        }),
        ('Orbital Parameters', {
            'fields': ('semi_major_axis', 'eccentricity', 'inclination', 'argument_of_periapsis', 'longitude_of_ascending_node', 'mean_anomaly')
        }),
        ('Physical Properties', {
            'fields': ('size', 'distance')
        }),
    )

# Admin configuration for Comet
class CometAdmin(admin.ModelAdmin):
    list_display = ('name', 'distance', 'orbital_period', 'eccentricity', 'last_updated')
    search_fields = ('name', 'nasa_id')
    list_filter = ('last_updated', 'eccentricity')
    readonly_fields = ('last_updated',)
    fieldsets = (
        ('General Information', {
            'fields': ('name', 'nasa_id', 'last_updated')
        }),
        ('Orbital Parameters', {
            'fields': ('orbital_period', 'eccentricity', 'inclination', 'argument_of_periapsis', 'longitude_of_ascending_node')
        }),
        ('Physical Properties', {
            'fields': ('distance',)
        }),
    )

# Admin configuration for Asteroid
class AsteroidAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'distance', 'is_potentially_hazardous', 'last_updated')
    search_fields = ('name', 'nasa_id')
    list_filter = ('is_potentially_hazardous', 'last_updated')
    readonly_fields = ('last_updated',)
    fieldsets = (
        ('General Information', {
            'fields': ('name', 'nasa_id', 'last_updated', 'is_potentially_hazardous')
        }),
        ('Physical Properties', {
            'fields': ('size', 'distance')
        }),
    )

# Admin configuration for CelestialBodyStats
class CelestialBodyStatsAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'total_bodies', 'total_planets', 'total_comets', 'total_asteroids', 'total_pha')
    readonly_fields = ('timestamp',)
    list_filter = ('timestamp',)

# Admin configuration for UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_opted_in', 'real_time_distance', 'critical_distance', 'points')
    search_fields = ('user__username', 'user__email')
    list_filter = ('is_opted_in',)
    readonly_fields = ('user',)

# Admin configuration for Topic
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Admin configuration for BlogPost
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('author', 'topic', 'status', 'time_of_submission')
    search_fields = ('author__username', 'topic__name', 'content')
    list_filter = ('status', 'topic')
    readonly_fields = ('time_of_submission',)
    fieldsets = (
        ('General Information', {
            'fields': ('author', 'topic', 'content', 'time_of_submission', 'status')
        }),
    )

# Registering the models in the admin panel
admin.site.register(Planet, PlanetAdmin)
admin.site.register(Comet, CometAdmin)
admin.site.register(Asteroid, AsteroidAdmin)
admin.site.register(CelestialBodyStats, CelestialBodyStatsAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
