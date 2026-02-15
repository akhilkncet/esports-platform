from rest_framework import serializers
from .models import (
    Tournament, Group, Match, MatchResult, Standings,
    FinalStage, FinalStageMatch, FinalStageResult
)
from teams.serializers import TeamListSerializer, TeamSerializer


class TournamentSerializer(serializers.ModelSerializer):
    organizer_id = serializers.IntegerField(write_only=True, required=False)
    organizer_name = serializers.CharField(source='organizer.username', read_only=True)
    groups_count = serializers.SerializerMethodField()

    class Meta:
        model = Tournament
        fields = [
            'id', 'name', 'description', 'organizer_id', 'organizer_name',
            'status', 'start_date', 'end_date', 'prize_pool', 'max_teams',
            'groups_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_groups_count(self, obj):
        return obj.groups.count()


class GroupSerializer(serializers.ModelSerializer):
    teams = TeamListSerializer(many=True, read_only=True)
    team_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    team_count = serializers.SerializerMethodField()
    tournament_name = serializers.CharField(source='tournament.name', read_only=True)

    class Meta:
        model = Group
        fields = [
            'id', 'tournament', 'tournament_name', 'name', 'teams',
            'team_ids', 'team_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_team_count(self, obj):
        return obj.teams.count()

    def validate_team_ids(self, value):
        if len(value) > 10:
            raise serializers.ValidationError("A group can have a maximum of 10 teams.")
        return value


class MatchResultSerializer(serializers.ModelSerializer):
    team = TeamListSerializer(read_only=True)
    team_id = serializers.IntegerField(write_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)
    team_tag = serializers.CharField(source='team.tag', read_only=True)

    class Meta:
        model = MatchResult
        fields = [
            'id', 'match', 'team', 'team_id', 'team_name', 'team_tag',
            'kill_points', 'placement', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MatchSerializer(serializers.ModelSerializer):
    results = MatchResultSerializer(many=True, read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)

    class Meta:
        model = Match
        fields = [
            'id', 'group', 'group_name', 'match_number', 'status',
            'scheduled_time', 'completed_time', 'results',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MatchResultCreateSerializer(serializers.Serializer):
    match_id = serializers.IntegerField()
    results = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False
    )

    def validate_results(self, value):
        for result in value:
            if 'team_id' not in result or 'kill_points' not in result:
                raise serializers.ValidationError(
                    "Each result must have 'team_id' and 'kill_points'."
                )
            if result['kill_points'] < 0:
                raise serializers.ValidationError("Kill points cannot be negative.")
        return value


class StandingsSerializer(serializers.ModelSerializer):
    team = TeamListSerializer(read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)
    team_tag = serializers.CharField(source='team.tag', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)

    class Meta:
        model = Standings
        fields = [
            'id', 'group', 'group_name', 'team', 'team_name', 'team_tag',
            'total_kills', 'matches_played', 'rank', 'qualification_status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FinalStageResultSerializer(serializers.ModelSerializer):
    team = TeamListSerializer(read_only=True)
    team_id = serializers.IntegerField(write_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)
    team_tag = serializers.CharField(source='team.tag', read_only=True)

    class Meta:
        model = FinalStageResult
        fields = [
            'id', 'match', 'team', 'team_id', 'team_name', 'team_tag',
            'kill_points', 'placement', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FinalStageMatchSerializer(serializers.ModelSerializer):
    results = FinalStageResultSerializer(many=True, read_only=True)

    class Meta:
        model = FinalStageMatch
        fields = [
            'id', 'final_stage', 'match_number', 'scheduled_time',
            'completed_time', 'is_completed', 'results',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FinalStageSerializer(serializers.ModelSerializer):
    tournament_name = serializers.CharField(source='tournament.name', read_only=True)
    participants = TeamListSerializer(many=True, read_only=True)
    winner = TeamListSerializer(read_only=True)
    matches = FinalStageMatchSerializer(many=True, read_only=True)

    class Meta:
        model = FinalStage
        fields = [
            'id', 'tournament', 'tournament_name', 'participants', 'winner',
            'start_date', 'end_date', 'is_completed', 'matches',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TeamAssignmentSerializer(serializers.Serializer):
    tournament_id = serializers.IntegerField()
    team_assignments = serializers.DictField(
        child=serializers.ListField(child=serializers.IntegerField())
    )

    def validate_team_assignments(self, value):
        expected_groups = {'A', 'B', 'C', 'D', 'E'}
        if set(value.keys()) != expected_groups:
            raise serializers.ValidationError(
                "Must provide assignments for exactly 5 groups: A, B, C, D, E."
            )
        
        for group, teams in value.items():
            if len(teams) != 10:
                raise serializers.ValidationError(
                    f"Group {group} must have exactly 10 teams, but has {len(teams)}."
                )
        
        all_teams = []
        for teams in value.values():
            all_teams.extend(teams)
        
        if len(all_teams) != len(set(all_teams)):
            raise serializers.ValidationError("A team cannot be assigned to multiple groups.")
        
        return value


class QualifyTop4Serializer(serializers.Serializer):
    team_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True,
        max_length=4
    )


class SelectWinnerSerializer(serializers.Serializer):
    winner_team_id = serializers.IntegerField(required=False)


class FinalStageResultCreateSerializer(serializers.Serializer):
    results = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False
    )

    def validate_results(self, value):
        for result in value:
            if 'team_id' not in result or 'kill_points' not in result:
                raise serializers.ValidationError(
                    "Each result must have 'team_id' and 'kill_points'."
                )
            if result['kill_points'] < 0:
                raise serializers.ValidationError("Kill points cannot be negative.")
        return value


class BulkMatchCreateSerializer(serializers.Serializer):
    matches_per_group = serializers.IntegerField(min_value=1, max_value=10, default=3)
    start_time = serializers.DateTimeField()
