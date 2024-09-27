import requests
from datetime import datetime, timedelta

API_KEY = 'WabOZ3Suz7jQnDroucIZHduxXz0EuAWO96H2vt0e'

def fetch_close_approaches(start_date=None, end_date=None, threshold_distance=100000, critical_distance=10000):
    """Fetches close approaches from NASA's API."""
    if not start_date:
        start_date = datetime.today().strftime('%Y-%m-%d')
    if not end_date:
        end_date = (datetime.today() + timedelta(days=7)).strftime('%Y-%m-%d')

    nasa_url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={API_KEY}'

    close_approaches = []
    critical_approaches = []

    try:
        response = requests.get(nasa_url)
        data = response.json()

        if 'near_earth_objects' in data:
            for date in data['near_earth_objects']:
                for neo in data['near_earth_objects'][date]:
                    distance_km = float(neo['close_approach_data'][0]['miss_distance']['kilometers'])

                    if distance_km < threshold_distance:
                        approach = {
                            'name': neo['name'],
                            'nasa_id': neo['id'],
                            'distance': distance_km,
                            'velocity': float(neo['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']),
                            'date': neo['close_approach_data'][0]['close_approach_date'],
                            'is_critical': distance_km < critical_distance,
                        }
                        close_approaches.append(approach)

                        if approach['is_critical']:
                            critical_approaches.append(approach)
        return close_approaches, critical_approaches
    except requests.RequestException as e:
        raise Exception(f"Error fetching data from NASA: {e}")
