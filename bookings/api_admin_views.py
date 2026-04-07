import requests
import threading
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Prediction
from datetime import date, timedelta

API_KEY = settings.FOOTBALL_API_KEY
BASE_URL = 'https://api.football-data.org/v4'
HEADERS = {'X-Auth-Token': API_KEY}

COMPETITIONS = {
    'Premier League': 'PL',
    'UEFA Champions League': 'CL',
    'La Liga': 'PD',
    'Bundesliga': 'BL1',
    'Serie A': 'SA',
    'Ligue 1': 'FL1',
    'Eredivisie': 'DED',
    'Championship': 'ELC',
}


def fetch_competition(league_name, comp_code, date_str, results, lock):
    """
    Fetches fixtures for one competition in a separate thread
    lock: prevents multiple threads writing to results at same time
    """
    try:
        response = requests.get(
            f'{BASE_URL}/competitions/{comp_code}/matches',
            headers=HEADERS,
            params={
                'dateFrom': date_str,
                'dateTo': date_str,
            },
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])

            if matches:
                competition = data.get('competition', {})
                league_logo = competition.get('emblem', '')

                with lock:
                    # lock: ensures only one thread writes at a time
                    # prevents data corruption when multiple threads
                    # try to update results simultaneously
                    results[league_name] = {
                        'logo': league_logo,
                        'fixtures': matches
                    }

    except Exception:
        pass


@staff_member_required
def api_football_view(request):
    date_str = request.GET.get('date', str(date.today()))

    try:
        selected_date = date.fromisoformat(date_str)
    except ValueError:
        selected_date = date.today()
        date_str = str(selected_date)

    yesterday = str(selected_date - timedelta(days=1))
    tomorrow = str(selected_date + timedelta(days=1))

    if request.method == 'POST':
        selected_matches = request.POST.getlist('matches')
        saved_count = 0

        for match_id in selected_matches:
            home_team = request.POST.get(f'home_{match_id}')
            away_team = request.POST.get(f'away_{match_id}')
            league = request.POST.get(f'league_{match_id}')
            league_logo = request.POST.get(f'league_logo_{match_id}', '')
            home_logo = request.POST.get(f'home_logo_{match_id}', '')
            away_logo = request.POST.get(f'away_logo_{match_id}', '')
            match_time = request.POST.get(f'time_{match_id}', '00:00')
            tip = request.POST.get(f'tip_{match_id}', 'Home Win')
            odds = request.POST.get(f'odds_{match_id}', '1.50')
            is_vip = request.POST.get(f'vip_{match_id}') == 'on'

            try:
                prediction, created = Prediction.objects.get_or_create(
                    date=date_str,
                    home_team=home_team,
                    away_team=away_team,
                    defaults={
                        'league': league,
                        'league_logo': league_logo,
                        'home_team_logo': home_logo,
                        'away_team_logo': away_logo,
                        'match_time': match_time,
                        'tip': tip,
                        'odds': float(odds),
                        'is_vip': is_vip,
                    }
                )

                if not created:
                    prediction.tip = tip
                    prediction.odds = float(odds)
                    prediction.is_vip = is_vip
                    prediction.save()

                saved_count += 1

            except Exception as e:
                messages.error(request, f'Error saving {home_team} vs {away_team}: {e}')

        messages.success(request, f'{saved_count} prediction(s) saved!')
        return redirect(f'/django-admin/api-football/?date={date_str}')

    # GET - fetch all competitions simultaneously using threads
    fixtures_by_league = {}
    lock = threading.Lock()
    # Lock: prevents race conditions when threads write to dictionary
    threads = []

    for league_name, comp_code in COMPETITIONS.items():
        thread = threading.Thread(
            target=fetch_competition,
            args=(league_name, comp_code, date_str, fixtures_by_league, lock)
            # each competition fetches in its own thread simultaneously
            # instead of waiting for each one to finish before starting next
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        # join: waits for ALL threads to finish before continuing

    total_fixtures = sum(
        len(league['fixtures']) for league in fixtures_by_league.values()
    )

    saved_predictions = Prediction.objects.filter(date=date_str)
    saved_matches = [
        f"{p.home_team}_{p.away_team}" for p in saved_predictions
    ]

    context = {
        'fixtures_by_league': fixtures_by_league,
        'selected_date': selected_date,
        'date_str': date_str,
        'yesterday': yesterday,
        'tomorrow': tomorrow,
        'saved_matches': saved_matches,
        'total_fixtures': total_fixtures,
    }

    return render(request, 'admin/api_football.html', context)