from rest_framework import serializers
from .models import Team
from accounts.serializers import UserSerializer


class TeamSerializer(serializers.ModelSerializer):
    manager = UserSerializer(read_only=True)
    manager_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'tag', 'manager', 'manager_id', 'logo',
            'country', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'tag': {'required': False},
            'logo': {'required': False},
            'country': {'required': False},
        }

    def validate_tag(self, value):
        if value and not value.isalnum():
            raise serializers.ValidationError("Tag must contain only letters and numbers.")
        return value.upper() if value else value
    
    def create(self, validated_data):
        if not validated_data.get('tag'):
            name = validated_data['name']
            base_tag = ''.join(c for c in name if c.isalnum())[:6].upper()
            
            tag = base_tag
            counter = 1
            while Team.objects.filter(tag=tag).exists():
                tag = f"{base_tag[:4]}{counter}"
                counter += 1
            
            validated_data['tag'] = tag
        
        return super().create(validated_data)


class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'tag', 'logo', 'country', 'is_active']


class BulkTeamCreateSerializer(serializers.Serializer):
    teams = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False,
        max_length=100
    )
    
    def validate_teams(self, value):
        team_names = []
        for team_data in value:
            if 'name' not in team_data:
                raise serializers.ValidationError("Each team must have a 'name' field.")
            team_names.append(team_data['name'])
        
        duplicates_in_payload = [name for name in set(team_names) if team_names.count(name) > 1]
        if duplicates_in_payload:
            raise serializers.ValidationError(f"Duplicate team names in payload: {', '.join(duplicates_in_payload)}")
        
        existing_teams = Team.objects.filter(name__in=team_names).values_list('name', flat=True)
        if existing_teams:
            raise serializers.ValidationError(f"Teams with these names already exist: {', '.join(existing_teams)}")
        
        return value
    
    def create(self, validated_data):
        teams_data = validated_data['teams']
        created_teams = []
        
        for team_data in teams_data:
            if not team_data.get('tag'):
                name = team_data['name']
                base_tag = ''.join(c for c in name if c.isalnum())[:6].upper()
                tag = base_tag
                counter = 1
                while Team.objects.filter(tag=tag).exists() or any(t.tag == tag for t in created_teams):
                    tag = f"{base_tag[:4]}{counter}"
                    counter += 1
                team_data['tag'] = tag
            
            team = Team.objects.create(
                name=team_data['name'],
                tag=team_data['tag'],
                manager_id=team_data.get('manager_id'),
                logo=team_data.get('logo', ''),
                country=team_data.get('country', ''),
                is_active=team_data.get('is_active', True)
            )
            created_teams.append(team)
        
        return created_teams
