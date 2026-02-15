from django.db import transaction
from django.db.models import Sum, Count
from django.utils import timezone
from .models import (
    Tournament, Group, Match, MatchResult, Standings,
    FinalStage, FinalStageMatch, FinalStageResult
)
from teams.models import Team


class TournamentService:
    @staticmethod
    @transaction.atomic
    def create_tournament_with_groups(tournament_data):
        tournament = Tournament.objects.create(**tournament_data)
        
        group_names = ['A', 'B', 'C', 'D', 'E']
        for name in group_names:
            Group.objects.create(tournament=tournament, name=name)
        
        return tournament

    @staticmethod
    @transaction.atomic
    def assign_teams_to_groups(tournament_id, team_assignments):
        tournament = Tournament.objects.get(id=tournament_id)
        
        if tournament.status not in ['draft', 'registration']:
            raise ValueError("Cannot assign teams after tournament has started.")
        
        for group in tournament.groups.all():
            group.teams.clear()
        
        for group_name, team_ids in team_assignments.items():
            group = tournament.groups.get(name=group_name)
            
            if len(team_ids) != 10:
                raise ValueError(f"Group {group_name} must have exactly 10 teams.")
            
            teams = Team.objects.filter(id__in=team_ids, is_active=True)
            if teams.count() != 10:
                raise ValueError(f"Some teams in group {group_name} are invalid or inactive.")
            
            group.teams.set(teams)
            
            for team in teams:
                Standings.objects.get_or_create(
                    group=group,
                    team=team,
                    defaults={
                        'total_kills': 0,
                        'matches_played': 0,
                        'rank': None,
                        'qualification_status': 'none'
                    }
                )
        
        return tournament


class MatchService:
    @staticmethod
    @transaction.atomic
    def submit_match_results(match_id, results_data):
        match = Match.objects.select_related('group').get(id=match_id)
        
        if match.status == 'completed':
            raise ValueError("Cannot modify results of a completed match.")
        
        MatchResult.objects.filter(match=match).delete()
        
        for result in results_data:
            team_id = result['team_id']
            kill_points = result['kill_points']
            placement = result.get('placement')
            
            if not match.group.teams.filter(id=team_id).exists():
                raise ValueError(f"Team {team_id} is not in this group.")
            
            MatchResult.objects.create(
                match=match,
                team_id=team_id,
                kill_points=kill_points,
                placement=placement
            )
        
        match.status = 'completed'
        match.completed_time = timezone.now()
        match.save()
        
        StandingsService.update_group_standings(match.group.id)
        
        return match


class StandingsService:
    @staticmethod
    @transaction.atomic
    def update_group_standings(group_id):
        group = Group.objects.get(id=group_id)
        
        for standing in group.standings.all():
            team_results = MatchResult.objects.filter(
                match__group=group,
                team=standing.team,
                match__status='completed'
            ).aggregate(
                total_kills=Sum('kill_points'),
                matches_played=Count('id', distinct=True)
            )
            
            standing.total_kills = team_results['total_kills'] or 0
            standing.matches_played = team_results['matches_played'] or 0
            standing.save()
        
        StandingsService.calculate_ranks(group_id)
        
        return group.standings.all().order_by('rank')

    @staticmethod
    def calculate_ranks(group_id):
        standings = Standings.objects.filter(group_id=group_id).order_by(
            '-total_kills', 'team__name'
        )
        
        current_rank = 1
        prev_kills = None
        
        for idx, standing in enumerate(standings, start=1):
            if prev_kills is not None and standing.total_kills != prev_kills:
                current_rank = idx
            
            standing.rank = current_rank
            standing.save(update_fields=['rank'])
            prev_kills = standing.total_kills

    @staticmethod
    @transaction.atomic
    def update_qualification_status(group_id):
        standings = Standings.objects.filter(group_id=group_id).order_by(
            '-total_kills', 'team__name'
        )
        
        standings.update(qualification_status='none')
        
        top_6 = standings[:6]
        for standing in top_6:
            standing.qualification_status = 'top_6'
            standing.save(update_fields=['qualification_status'])
        
        return standings

    @staticmethod
    @transaction.atomic
    def select_top_4_from_top_6(group_id, selected_team_ids):
        if len(selected_team_ids) != 4:
            raise ValueError("Must select exactly 4 teams.")
        
        standings = Standings.objects.filter(
            group_id=group_id,
            qualification_status='top_6'
        )
        
        if standings.count() < 6:
            raise ValueError("Must have top 6 qualified before selecting top 4.")
        
        top_6_team_ids = set(standings.values_list('team_id', flat=True))
        if not set(selected_team_ids).issubset(top_6_team_ids):
            raise ValueError("Selected teams must be from the top 6.")
        
        Standings.objects.filter(
            group_id=group_id,
            team_id__in=selected_team_ids
        ).update(qualification_status='top_4')
        
        return Standings.objects.filter(group_id=group_id, qualification_status='top_4')

    @staticmethod
    @transaction.atomic
    def select_group_winner(group_id, winner_team_id):
        top_4_standing = Standings.objects.filter(
            group_id=group_id,
            qualification_status='top_4',
            team_id=winner_team_id
        ).first()
        
        if not top_4_standing:
            raise ValueError("Winner must be from the top 4 teams.")
        
        top_4_standing.qualification_status = 'winner'
        top_4_standing.save(update_fields=['qualification_status'])
        
        return top_4_standing


class FinalStageService:
    @staticmethod
    @transaction.atomic
    def create_final_stage(tournament_id):
        tournament = Tournament.objects.get(id=tournament_id)
        
        winners = Standings.objects.filter(
            group__tournament=tournament,
            qualification_status='winner'
        ).select_related('team')
        
        if winners.count() != 5:
            raise ValueError(
                f"Need exactly 5 group winners to create final stage. "
                f"Currently have {winners.count()}."
            )
        
        final_stage, created = FinalStage.objects.get_or_create(
            tournament=tournament,
            defaults={'start_date': timezone.now()}
        )
        
        winner_teams = [w.team for w in winners]
        final_stage.participants.set(winner_teams)
        
        tournament.status = 'final_stage'
        tournament.save(update_fields=['status'])
        
        return final_stage

    @staticmethod
    @transaction.atomic
    def submit_final_match_results(match_id, results_data):
        match = FinalStageMatch.objects.get(id=match_id)
        
        if match.is_completed:
            raise ValueError("Cannot modify results of a completed match.")
        
        FinalStageResult.objects.filter(match=match).delete()
        
        for result in results_data:
            FinalStageResult.objects.create(
                match=match,
                team_id=result['team_id'],
                kill_points=result['kill_points'],
                placement=result.get('placement')
            )
        
        match.is_completed = True
        match.completed_time = timezone.now()
        match.save()
        
        return match

    @staticmethod
    @transaction.atomic
    def determine_final_winner(final_stage_id):
        final_stage = FinalStage.objects.get(id=final_stage_id)
        
        team_kills = {}
        for result in FinalStageResult.objects.filter(
            match__final_stage=final_stage,
            match__is_completed=True
        ):
            team_id = result.team_id
            team_kills[team_id] = team_kills.get(team_id, 0) + result.kill_points
        
        if not team_kills:
            raise ValueError("No completed matches in final stage.")
        
        winner_team_id = max(team_kills, key=team_kills.get)
        winner_team = Team.objects.get(id=winner_team_id)
        
        final_stage.winner = winner_team
        final_stage.is_completed = True
        final_stage.end_date = timezone.now()
        final_stage.save()
        
        final_stage.tournament.status = 'completed'
        final_stage.tournament.save(update_fields=['status'])
        
        return final_stage


class QualificationService:
    @staticmethod
    def get_qualification_summary(tournament_id):
        tournament = Tournament.objects.get(id=tournament_id)
        summary = {}
        
        for group in tournament.groups.all():
            standings = Standings.objects.filter(group=group).order_by('-total_kills')
            
            summary[f"Group {group.name}"] = {
                'top_6': list(standings.filter(qualification_status='top_6').values(
                    'team__name', 'team__tag', 'total_kills', 'rank'
                )),
                'top_4': list(standings.filter(qualification_status='top_4').values(
                    'team__name', 'team__tag', 'total_kills', 'rank'
                )),
                'winner': standings.filter(qualification_status='winner').first()
            }
        
        return summary

    @staticmethod
    @transaction.atomic
    def auto_qualify_top_6(group_id):
        StandingsService.update_group_standings(group_id)
        return StandingsService.update_qualification_status(group_id)

    @staticmethod
    @transaction.atomic
    def auto_qualify_top_4(group_id):
        standings = Standings.objects.filter(
            group_id=group_id
        ).order_by('-total_kills', 'team__name')[:4]
        
        selected_team_ids = [s.team_id for s in standings]
        return StandingsService.select_top_4_from_top_6(group_id, selected_team_ids)

    @staticmethod
    @transaction.atomic
    def auto_select_group_winner(group_id):
        top_4 = Standings.objects.filter(
            group_id=group_id,
            qualification_status='top_4'
        ).order_by('-total_kills', 'team__name').first()
        
        if not top_4:
            raise ValueError("No top 4 teams available.")
        
        return StandingsService.select_group_winner(group_id, top_4.team_id)
