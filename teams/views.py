from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Team
from .serializers import TeamSerializer, TeamListSerializer, BulkTeamCreateSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'country']
    search_fields = ['name', 'tag']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TeamListSerializer
        return TeamSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        teams = self.queryset.filter(is_active=True)
        serializer = TeamListSerializer(teams, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        team = self.get_object()
        team.is_active = False
        team.save()
        serializer = self.get_serializer(team)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        team = self.get_object()
        team.is_active = True
        team.save()
        serializer = self.get_serializer(team)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], serializer_class=BulkTeamCreateSerializer)
    def bulk_create(self, request):
        serializer = BulkTeamCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            created_teams = serializer.save()
            response_serializer = TeamListSerializer(created_teams, many=True)
            return Response({
                'message': f'{len(created_teams)} teams created successfully',
                'teams': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
