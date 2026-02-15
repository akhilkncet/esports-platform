import os
import sys
import django
import requests
from datetime import datetime, timedelta
from time import sleep

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'esports_platform.settings')
django.setup()

from django.contrib.auth import get_user_model
from teams.models import Team
from tournaments.models import Tournament, Group, Match, FinalStage, FinalStageMatch
from tournaments.services import (
    TournamentService, MatchService, QualificationService, FinalStageService
)

User = get_user_model()


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")


def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_info(text):
    print(f"{Colors.BLUE}➤ {text}{Colors.END}")


def print_step(step, text):
    print(f"\n{Colors.BOLD}{Colors.YELLOW}[STEP {step}] {text}{Colors.END}")


class TournamentWorkflowTest:
    def __init__(self):
        self.organizer = None
        self.teams = []
        self.tournament = None
        self.groups = []
        self.final_stage = None
        
    def cleanup_previous_data(self):
        print_step(0, "Cleaning Up Previous Test Data")
        
        Team.objects.filter(name__startswith='Team ').delete()
        Tournament.objects.filter(name='Championship 2026').delete()
        User.objects.filter(username='test_organizer').delete()
        
        print_success("Previous test data cleaned")
    
    def step_1_create_organizer(self):
        print_step(1, "Create Organizer Account")
        
        self.organizer, created = User.objects.get_or_create(
            username='test_organizer',
            defaults={
                'email': 'organizer@esports.com',
                'is_organizer': True,
                'first_name': 'Test',
                'last_name': 'Organizer'
            }
        )
        
        if created:
            self.organizer.set_password('password123')
            self.organizer.save()
            print_success(f"Created organizer: {self.organizer.username}")
        else:
            print_info(f"Using existing organizer: {self.organizer.username}")
    
    def step_2_create_50_teams(self):
        print_step(2, "Create 50 Teams (10 per group)")
        
        team_names = [
            "Team Alpha", "Team Beta", "Team Gamma", "Team Delta", "Team Epsilon",
            "Team Zeta", "Team Eta", "Team Theta", "Team Iota", "Team Kappa",
            "Team Lambda", "Team Mu", "Team Nu", "Team Xi", "Team Omicron",
            "Team Pi", "Team Rho", "Team Sigma", "Team Tau", "Team Upsilon",
            "Team Phi", "Team Chi", "Team Psi", "Team Omega", "Team Phoenix",
            "Team Dragon", "Team Tiger", "Team Lion", "Team Eagle", "Team Falcon",
            "Team Shark", "Team Wolf", "Team Bear", "Team Panther", "Team Viper",
            "Team Thunder", "Team Lightning", "Team Storm", "Team Blaze", "Team Frost",
            "Team Shadow", "Team Phantom", "Team Spirit", "Team Legend", "Team Titan",
            "Team Warrior", "Team Knight", "Team Champion", "Team Victory", "Team Glory"
        ]
        
        for i, name in enumerate(team_names, 1):
            team, created = Team.objects.get_or_create(
                name=name,
                defaults={
                    'tag': f"T{i:02d}",
                    'manager': self.organizer,
                    'is_active': True,
                    'country': 'USA'
                }
            )
            self.teams.append(team)
        
        print_success(f"Created {len(self.teams)} teams")
    
    def step_3_create_tournament(self):
        print_step(3, "Create Tournament with 5 Groups")
        
        tournament_data = {
            'name': 'Championship 2026',
            'description': 'Annual esports championship with 50 teams',
            'organizer': self.organizer,
            'status': 'draft',
            'start_date': datetime.now() + timedelta(days=1),
            'end_date': datetime.now() + timedelta(days=30),
            'prize_pool': 500000.00,
            'max_teams': 50
        }
        
        self.tournament = TournamentService.create_tournament_with_groups(tournament_data)
        self.groups = list(self.tournament.groups.all().order_by('name'))
        
        print_success(f"Created tournament: {self.tournament.name}")
        print_info(f"Groups created: {[g.name for g in self.groups]}")
        
        assert len(self.groups) == 5, "Tournament must have exactly 5 groups"
        print_success("✓ Verified: 5 groups created")
    
    def step_4_assign_teams_to_groups(self):
        print_step(4, "Assign Teams to Groups (10 per group)")
        
        team_assignments = {
            'A': [self.teams[i].id for i in range(0, 10)],
            'B': [self.teams[i].id for i in range(10, 20)],
            'C': [self.teams[i].id for i in range(20, 30)],
            'D': [self.teams[i].id for i in range(30, 40)],
            'E': [self.teams[i].id for i in range(40, 50)]
        }
        
        TournamentService.assign_teams_to_groups(self.tournament.id, team_assignments)
        
        for group in self.groups:
            group.refresh_from_db()
            team_count = group.teams.count()
            print_info(f"Group {group.name}: {team_count} teams")
            assert team_count == 10, f"Group {group.name} must have 10 teams"
        
        print_success("✓ All groups have exactly 10 teams")
    
    def step_5_create_matches(self):
        print_step(5, "Create Matches (3 per group = 15 total)")
        
        match_count = 0
        for group in self.groups:
            for match_num in range(1, 4):
                Match.objects.create(
                    group=group,
                    match_number=match_num,
                    scheduled_time=datetime.now() + timedelta(days=match_num),
                    status='scheduled'
                )
                match_count += 1
        
        print_success(f"Created {match_count} matches")
    
    def step_6_submit_match_results(self):
        print_step(6, "Submit Match Results for All Matches")
        
        for group in self.groups:
            print_info(f"Processing Group {group.name} matches...")
            matches = group.matches.all().order_by('match_number')
            
            for match in matches:
                teams = list(group.teams.all())
                results_data = []
                
                for i, team in enumerate(teams):
                    kill_points = (10 - i) * match.match_number * 2 + (ord(group.name) - ord('A')) * 2
                    results_data.append({
                        'team_id': team.id,
                        'kill_points': kill_points,
                        'placement': i + 1
                    })
                
                MatchService.submit_match_results(match.id, results_data)
            
            print_success(f"  Submitted results for Group {group.name}")
        
        print_success("All match results submitted")
    
    def step_7_view_standings(self):
        print_step(7, "View Group Standings (Ranked by Kills)")
        
        for group in self.groups:
            standings = group.standings.all().order_by('rank')[:3]
            print_info(f"Group {group.name} - Top 3:")
            for standing in standings:
                print(f"    Rank {standing.rank}: {standing.team.tag} - {standing.total_kills} kills")
    
    def step_8_qualify_top_6(self):
        print_step(8, "Qualify Top 6 Teams per Group")
        
        for group in self.groups:
            QualificationService.auto_qualify_top_6(group.id)
            top_6 = group.standings.filter(qualification_status='top_6').count()
            print_success(f"Group {group.name}: {top_6} teams qualified to top 6")
            assert top_6 == 6, f"Group {group.name} must have exactly 6 in top 6"
    
    def step_9_qualify_top_4(self):
        print_step(9, "Qualify Top 4 from Top 6")
        
        for group in self.groups:
            QualificationService.auto_qualify_top_4(group.id)
            top_4 = group.standings.filter(qualification_status='top_4').count()
            print_success(f"Group {group.name}: {top_4} teams qualified to top 4")
            assert top_4 == 4, f"Group {group.name} must have exactly 4 in top 4"
    
    def step_10_select_winners(self):
        print_step(10, "Select 1 Winner from Top 4 (Each Group)")
        
        winners = []
        for group in self.groups:
            winner_standing = QualificationService.auto_select_group_winner(group.id)
            winners.append(winner_standing.team)
            print_success(f"Group {group.name} Winner: {winner_standing.team.tag} ({winner_standing.total_kills} kills)")
        
        assert len(winners) == 5, "Must have exactly 5 group winners"
        print_success("✓ All 5 group winners selected")
        
        return winners
    
    def step_11_create_final_stage(self):
        print_step(11, "Create Final Stage with 5 Winners")
        
        self.final_stage = FinalStageService.create_final_stage(self.tournament.id)
        participants = self.final_stage.participants.all()
        
        print_success(f"Final stage created with {participants.count()} participants")
        print_info("Finalists:")
        for team in participants:
            print(f"    - {team.tag}")
        
        assert participants.count() == 5, "Final stage must have exactly 5 participants"
        print_success("✓ Verified: 5 finalists")
    
    def step_12_create_final_matches(self):
        print_step(12, "Create Final Stage Matches")
        
        for match_num in range(1, 4):
            FinalStageMatch.objects.create(
                final_stage=self.final_stage,
                match_number=match_num,
                scheduled_time=datetime.now() + timedelta(days=20 + match_num),
                is_completed=False
            )
        
        print_success("Created 3 final stage matches")
    
    def step_13_submit_final_results(self):
        print_step(13, "Submit Final Stage Match Results")
        
        final_matches = self.final_stage.matches.all().order_by('match_number')
        finalists = list(self.final_stage.participants.all())
        
        for match in final_matches:
            results_data = []
            for i, team in enumerate(finalists):
                kill_points = (5 - i) * match.match_number * 5
                results_data.append({
                    'team_id': team.id,
                    'kill_points': kill_points,
                    'placement': i + 1
                })
            
            FinalStageService.submit_final_match_results(match.id, results_data)
            print_success(f"  Submitted results for Final Match {match.match_number}")
    
    def step_14_determine_winner(self):
        print_step(14, "Determine Overall Tournament Winner")
        
        self.final_stage = FinalStageService.determine_final_winner(self.final_stage.id)
        
        print_success(f"🏆 TOURNAMENT WINNER: {self.final_stage.winner.tag}")
        print_info(f"Tournament status: {self.tournament.status}")
        
        self.tournament.refresh_from_db()
        assert self.tournament.status == 'completed', "Tournament must be marked as completed"
        print_success("✓ Tournament marked as completed")
    
    def step_15_view_final_leaderboard(self):
        print_step(15, "View Final Stage Leaderboard")
        
        from django.db.models import Sum
        from tournaments.models import FinalStageResult
        
        results = FinalStageResult.objects.filter(
            match__final_stage=self.final_stage,
            match__is_completed=True
        ).values('team__id', 'team__tag').annotate(
            total_kills=Sum('kill_points')
        ).order_by('-total_kills')
        
        print_info("Final Leaderboard:")
        for idx, result in enumerate(results, 1):
            winner_mark = "🏆 " if idx == 1 else "   "
            print(f"{winner_mark}{idx}. {result['team__tag']} - {result['total_kills']} kills")
    
    def run_complete_workflow(self):
        print_header("COMPLETE TOURNAMENT WORKFLOW TEST")
        print_info("Testing all 15 steps of the tournament system\n")
        
        try:
            self.cleanup_previous_data()
            self.step_1_create_organizer()
            self.step_2_create_50_teams()
            self.step_3_create_tournament()
            self.step_4_assign_teams_to_groups()
            self.step_5_create_matches()
            self.step_6_submit_match_results()
            self.step_7_view_standings()
            self.step_8_qualify_top_6()
            self.step_9_qualify_top_4()
            self.step_10_select_winners()
            self.step_11_create_final_stage()
            self.step_12_create_final_matches()
            self.step_13_submit_final_results()
            self.step_14_determine_winner()
            self.step_15_view_final_leaderboard()
            
            print_header("TEST COMPLETED SUCCESSFULLY! ✓")
            print_success("All 15 steps executed without errors")
            print_success("Tournament workflow is fully functional")
            
            print_info("\nSummary:")
            print(f"  • 50 teams created across 5 groups")
            print(f"  • 15 group stage matches completed")
            print(f"  • 5 group winners advanced to finals")
            print(f"  • 3 final stage matches completed")
            print(f"  • Winner: {self.final_stage.winner.tag} 🏆")
            
        except AssertionError as e:
            print_error(f"Assertion failed: {str(e)}")
            return False
        except Exception as e:
            print_error(f"Error occurred: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
        
        return True


if __name__ == '__main__':
    print(f"\n{Colors.BOLD}Starting Tournament Workflow Test...{Colors.END}\n")
    
    test = TournamentWorkflowTest()
    success = test.run_complete_workflow()
    
    if success:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! 🎉{Colors.END}\n")
        sys.exit(0)
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ TESTS FAILED{Colors.END}\n")
        sys.exit(1)
