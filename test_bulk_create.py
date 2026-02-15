import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'esports_platform.settings')
django.setup()

from teams.serializers import BulkTeamCreateSerializer

teams_data = {
    "teams": [
        {"name": f"Test Team {i}", "country": "USA", "is_active": True}
        for i in range(1, 11)
    ]
}

serializer = BulkTeamCreateSerializer(data=teams_data)

if serializer.is_valid():
    created_teams = serializer.save()
    print(f"✓ Successfully created {len(created_teams)} teams")
    for team in created_teams:
        print(f"  - {team.name} (Tag: {team.tag})")
else:
    print(f"✗ Validation errors: {serializer.errors}")
