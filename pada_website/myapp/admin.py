from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Voie, Suggestion

 
@admin.register(Voie)
class VoieAdmin(admin.ModelAdmin):
    list_display = ('entites_territoriales_2', 'nom_voies', 'quartier', 'description', 'has_personnalite_photo_display')
    readonly_fields = ('has_personnalite_photo_display',)
    search_fields = ('nom_voies', 'quartier', 'entites_territoriales_2')
    list_filter = ('quartier', 'entites_territoriales_2')
    
    fieldsets = (
        (None, {
            'fields': ('nom_voies', 'quartier', 'description', 'typologie')
        }),
        ('Personnalité', {
            'fields': ('photo_personnalite',),
            'classes': ('collapse',)
        }),
        ('Coordonnées', {
            'fields': ('X', 'Y'),
            'classes': ('collapse',)
        }),
        ('Autres informations', {
            'fields': ('qr_code', 'entites_territoriales_2'),
            'classes': ('collapse',)
        }),
    )
    
    def has_personnalite_photo_display(self, obj):
        return obj.has_personnalite_photo
    has_personnalite_photo_display.boolean = True
    has_personnalite_photo_display.short_description = 'A une photo'
    
    
@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('nom_voie', 'date_creation', 'short_suggestion')
    list_filter = ('date_creation',)
    search_fields = ('nom_voie', 'suggestion')
    
    def short_suggestion(self, obj):
        return obj.suggestion[:50] + '...' if len(obj.suggestion) > 50 else obj.suggestion
    short_suggestion.short_description = 'Suggestion'