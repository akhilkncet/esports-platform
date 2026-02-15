from django.contrib import admin
from .models import (
    Tournament, Group, Match, MatchResult, Standings,
    FinalStage, FinalStageMatch, FinalStageResult
)


class GroupInline(admin.TabularInline):
    model = Group
    extra = 0
    show_change_link = True


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'organizer', 'status', 'start_date', 'end_date', 'created_at']
    list_filter = ['status', 'start_date', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-start_date']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [GroupInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'organizer')
        }),
        ('Tournament Details', {
            'fields': ('status', 'start_date', 'end_date', 'prize_pool', 'max_teams')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['tournament', 'name', 'get_team_count', 'created_at']
    list_filter = ['tournament', 'name']
    search_fields = ['tournament__name']
    filter_horizontal = ['teams']
    readonly_fields = ['created_at', 'updated_at']


class MatchResultInline(admin.TabularInline):
    model = MatchResult
    extra = 0


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['group', 'match_number', 'status', 'scheduled_time', 'completed_time']
    list_filter = ['status', 'group', 'scheduled_time']
    search_fields = ['group__tournament__name']
    ordering = ['scheduled_time']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [MatchResultInline]


@admin.register(MatchResult)
class MatchResultAdmin(admin.ModelAdmin):
    list_display = ['match', 'team', 'kill_points', 'placement', 'created_at']
    list_filter = ['match__group', 'team']
    search_fields = ['team__name', 'match__group__tournament__name']
    ordering = ['-kill_points']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Standings)
class StandingsAdmin(admin.ModelAdmin):
    list_display = ['group', 'team', 'rank', 'total_kills', 'matches_played', 'qualification_status']
    list_filter = ['group', 'qualification_status']
    search_fields = ['team__name', 'group__tournament__name']
    ordering = ['group', 'rank']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(FinalStage)
class FinalStageAdmin(admin.ModelAdmin):
    list_display = ['tournament', 'winner', 'is_completed', 'start_date', 'end_date']
    list_filter = ['is_completed', 'start_date']
    search_fields = ['tournament__name']
    filter_horizontal = ['participants']
    readonly_fields = ['created_at', 'updated_at']


class FinalStageResultInline(admin.TabularInline):
    model = FinalStageResult
    extra = 0


@admin.register(FinalStageMatch)
class FinalStageMatchAdmin(admin.ModelAdmin):
    list_display = ['final_stage', 'match_number', 'is_completed', 'scheduled_time', 'completed_time']
    list_filter = ['is_completed', 'final_stage']
    search_fields = ['final_stage__tournament__name']
    ordering = ['match_number']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [FinalStageResultInline]


@admin.register(FinalStageResult)
class FinalStageResultAdmin(admin.ModelAdmin):
    list_display = ['match', 'team', 'kill_points', 'placement', 'created_at']
    list_filter = ['match__final_stage', 'team']
    search_fields = ['team__name', 'match__final_stage__tournament__name']
    ordering = ['-kill_points']
    readonly_fields = ['created_at', 'updated_at']

