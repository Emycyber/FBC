import requests
import threading
from django.core.cache import cache
from django.conf import settings
from datetime import date

API_KEY = settings.FOOTBALL_API_KEY
BASE_URL = 'https://v3.football.api-sports.io'
HEADERS = {'x-apisports-key': API_KEY}

LEAGUE_IDS = {
    'Premier League': 39,
    'La Liga': 140,
    'Serie A': 135,
    'Bundesliga': 78,
    'Ligue 1': 61,
    'Champions League': 2,
}

def fetch_league(league_id, date_str, results):
    # this function runs in a separate thread
    # for each league simultaneously
    try:
        
        # current_year = date.today().year
        # automatically gets current year
        # no need to hardcode 2024
        
        response = requests.get(
            f'{BASE_URL}/fixtures',
            headers=HEADERS,
            params={
                'date': date_str,
                'league': league_id,
                'season': 2025,
            },
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            results.extend(data.get('response', []))
            # extend: adds to shared results list
    except requests.exceptions.RequestException:
        pass


def get_fixtures(date_str=None):
    if date_str is None:
        date_str = str(date.today())

    cache_key = f'fixtures_{date_str}'
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return cached_data
        # return instantly if cached

    all_fixtures = []
    threads = []

    for league_id in LEAGUE_IDS.values():
        thread = threading.Thread(
            target=fetch_league,
            args=(league_id, date_str, all_fixtures)
            # args: arguments passed to fetch_league function
            # each league runs in its own thread simultaneously
        )
        threads.append(thread)
        thread.start()
        # start: begins the thread immediately

    for thread in threads:
        thread.join()
        # join: waits for all threads to finish
        # before continuing

    cache.set(cache_key, all_fixtures, 60 * 30)
    # cache for 30 minutes

    return all_fixtures

def get_team_logo(team_name):
    # searches API Football for a team and returns their logo URL
    cache_key = f'team_logo_{team_name.lower().replace(" ", "_")}'
    cached = cache.get(cache_key)

    if cached:
        return cached

    try:
        response = requests.get(
            f'{BASE_URL}/teams',
            headers=HEADERS,
            params={'search': team_name},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            teams = data.get('response', [])
            if teams:
                logo = teams[0]['team']['logo']
                cache.set(cache_key, logo, 60 * 60 * 24)
                # cache logo for 24 hours
                return logo
    except:
        pass
    return ''