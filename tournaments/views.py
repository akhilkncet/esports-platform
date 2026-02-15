from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import (
    Tournament, Group, Match, MatchResult, Standings,
    FinalStage, FinalStageMatch, FinalStageResult
)
from .serializers import (
    TournamentSerializer, GroupSerializer, MatchSerializer,
    MatchResultSerializer, StandingsSerializer, FinalStageSerializer,
    FinalStageMatchSerializer, MatchResultCreateSerializer,
    TeamAssignmentSerializer, QualifyTop4Serializer, SelectWinnerSerializer,
    FinalStageResultCreateSerializer, BulkMatchCreateSerializer
)
from .services import (
    TournamentService, MatchService, StandingsService,
    FinalStageService, QualificationService
)


class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'organizer']
    search_fields = ['name', 'description']
    ordering_fields = ['start_date', 'created_at']
    ordering = ['-start_date']
    
    def perform_create(self, serializer):
        tournament_data = serializer.validated_data
        if 'organizer_id' not in tournament_data:
            tournament_data['organizer'] = self.request.user
        else:
            organizer_id = tournament_data.pop('organizer_id')
            tournament_data['organizer_id'] = organizer_id
        
        tournament = TournamentService.create_tournament_with_groups(tournament_data)
        serializer.instance = tournament
    
    @action(detail=True, methods=['post'], serializer_class=TeamAssignmentSerializer)
    def assign_teams(self, request, pk=None):
        tournament = self.get_object()
        serializer = TeamAssignmentSerializer(data={
            'tournament_id': tournament.id,
            'team_assignments': request.data.get('team_assignments', {})
        })
        
        if serializer.is_valid():
            try:
                TournamentService.assign_teams_to_groups(
                    tournament.id,
                    serializer.validated_data['team_assignments']
                )
                return Response({
                    'message': 'Teams assigned successfully',
                    'tournament': TournamentSerializer(tournament).data
                }, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], serializer_class=BulkMatchCreateSerializer)
    def create_matches(self, request, pk=None):
        tournament = self.get_object()
        serializer = BulkMatchCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        matches_per_group = serializer.validated_data['matches_per_group']
        start_time = serializer.validated_data['start_time']
        
        groups = tournament.groups.all().order_by('name')
        if groups.count() != 5:
            return Response({'error': 'Tournament must have exactly 5 groups'}, status=status.HTTP_400_BAD_REQUEST)
        
        created_matches = []
        from datetime import timedelta
        
        for group in groups:
            for match_num in range(1, matches_per_group + 1):
                match = Match.objects.create(
                    group=group,
                    match_number=match_num,
                    status='scheduled',
                    scheduled_time=start_time + timedelta(hours=(group.id - 1) * matches_per_group + match_num - 1)
                )
                created_matches.append(match)
        
        return Response({
            'message': f'{len(created_matches)} matches created successfully',
            'matches_per_group': matches_per_group,
            'total_matches': len(created_matches),
            'matches': MatchSerializer(created_matches, many=True).data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def groups(self, request, pk=None):
        tournament = self.get_object()
        groups = tournament.groups.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def standings(self, request, pk=None):
        tournament = self.get_object()
        all_standings = Standings.objects.filter(
            group__tournament=tournament
        ).select_related('team', 'group').order_by('group__name', 'rank')
        
        serializer = StandingsSerializer(all_standings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def qualification_summary(self, request, pk=None):
        tournament = self.get_object()
        summary = QualificationService.get_qualification_summary(tournament.id)
        return Response(summary)
    
    @action(detail=True, methods=['post'])
    def create_final_stage(self, request, pk=None):
        tournament = self.get_object()
        try:
            final_stage = FinalStageService.create_final_stage(tournament.id)
            serializer = FinalStageSerializer(final_stage)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tournament', 'name']
    
    @action(detail=True, methods=['get'])
    def standings(self, request, pk=None):
        group = self.get_object()
        standings = group.standings.all().order_by('rank')
        serializer = StandingsSerializer(standings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_standings(self, request, pk=None):
        group = self.get_object()
        standings = StandingsService.update_group_standings(group.id)
        serializer = StandingsSerializer(standings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def qualify_top_6(self, request, pk=None):
        group = self.get_object()
        standings = QualificationService.auto_qualify_top_6(group.id)
        serializer = StandingsSerializer(standings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], serializer_class=QualifyTop4Serializer)
    def qualify_top_4(self, request, pk=None):
        group = self.get_object()
        team_ids = request.data.get('team_ids')
        
        try:
            if team_ids:
                standings = StandingsService.select_top_4_from_top_6(group.id, team_ids)
            else:
                standings = QualificationService.auto_qualify_top_4(group.id)
            
            serializer = StandingsSerializer(standings, many=True)
            return Response(serializer.data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], serializer_class=SelectWinnerSerializer)
    def select_winner(self, request, pk=None):
        group = self.get_object()
        winner_team_id = request.data.get('winner_team_id')
        
        if not winner_team_id:
            try:
                standing = QualificationService.auto_select_group_winner(group.id)
                serializer = StandingsSerializer(standing)
                return Response(serializer.data)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            standing = StandingsService.select_group_winner(group.id, winner_team_id)
            serializer = StandingsSerializer(standing)
            return Response(serializer.data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def matches(self, request, pk=None):
        group = self.get_object()
        matches = group.matches.all()
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['group', 'status']
    ordering_fields = ['scheduled_time', 'match_number']
    ordering = ['scheduled_time']
    
    @action(detail=True, methods=['post'], serializer_class=MatchResultCreateSerializer)
    def submit_results(self, request, pk=None):
        match = self.get_object()
        serializer = MatchResultCreateSerializer(data={
            'match_id': match.id,
            'results': request.data.get('results', [])
        })
        
        if serializer.is_valid():
            try:
                updated_match = MatchService.submit_match_results(
                    match.id,
                    serializer.validated_data['results']
                )
                return Response({
                    'message': 'Results submitted successfully',
                    'match': MatchSerializer(updated_match).data
                }, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        match = self.get_object()
        results = match.results.all()
        serializer = MatchResultSerializer(results, many=True)
        return Response(serializer.data)


class StandingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Standings.objects.all()
    serializer_class = StandingsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['group', 'team', 'qualification_status']
    ordering_fields = ['rank', 'total_kills']
    ordering = ['group', 'rank']


class FinalStageViewSet(viewsets.ModelViewSet):
    queryset = FinalStage.objects.all()
    serializer_class = FinalStageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=True, methods=['post'])
    def determine_winner(self, request, pk=None):
        final_stage = self.get_object()
        try:
            updated_final_stage = FinalStageService.determine_final_winner(final_stage.id)
            serializer = self.get_serializer(updated_final_stage)
            return Response(serializer.data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def leaderboard(self, request, pk=None):
        final_stage = self.get_object()
        
        from django.db.models import Sum
        results = FinalStageResult.objects.filter(
            match__final_stage=final_stage,
            match__is_completed=True
        ).values('team__id', 'team__name', 'team__tag').annotate(
            total_kills=Sum('kill_points')
        ).order_by('-total_kills')
        
        return Response(list(results))


class FinalStageMatchViewSet(viewsets.ModelViewSet):
    queryset = FinalStageMatch.objects.all()
    serializer_class = FinalStageMatchSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['final_stage', 'is_completed']
    
    @action(detail=True, methods=['post'], serializer_class=FinalStageResultCreateSerializer)
    def submit_results(self, request, pk=None):
        match = self.get_object()
        results_data = request.data.get('results', [])
        
        try:
            updated_match = FinalStageService.submit_final_match_results(
                match.id,
                results_data
            )
            serializer = self.get_serializer(updated_match)
            return Response(serializer.data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
