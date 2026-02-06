import pandas as pd
import numpy as np
from datetime import datetime, time


def get_traffic_multiplier(road_type, hour_of_day, day_of_week):
    """
    Simulate traffic congestion multiplier based on time and road type

    Args:
        road_type: Type of road (motorway, primary, residential, etc.)
        hour_of_day: Hour (0-23)
        day_of_week: Day (0=Monday, 6=Sunday)

    Returns:
        Multiplier for travel time (1.0 = no traffic, 2.0 = twice as long)
    """
    base_multiplier = 1.0

    # Weekend vs weekday
    is_weekend = day_of_week >= 5

    # Rush hour patterns (weekdays only)
    if not is_weekend:
        # Morning rush (7-9 AM)
        if 7 <= hour_of_day <= 9:
            if road_type in ['motorway', 'trunk', 'primary']:
                base_multiplier = 1.8  # Heavy congestion
            elif road_type in ['secondary', 'tertiary']:
                base_multiplier = 1.4

        # Evening rush (5-7 PM)
        elif 17 <= hour_of_day <= 19:
            if road_type in ['motorway', 'trunk', 'primary']:
                base_multiplier = 2.0  # Heaviest congestion
            elif road_type in ['secondary', 'tertiary']:
                base_multiplier = 1.5

        # Midday moderate traffic
        elif 12 <= hour_of_day <= 16:
            if road_type in ['motorway', 'trunk', 'primary']:
                base_multiplier = 1.3

    # Weekend moderate traffic (different pattern)
    else:
        # Weekend afternoon (shopping, leisure)
        if 14 <= hour_of_day <= 18:
            if road_type in ['secondary', 'tertiary', 'residential']:
                base_multiplier = 1.3

    # Late night (minimal traffic)
    if hour_of_day >= 22 or hour_of_day <= 5:
        base_multiplier = 0.9  # Actually faster than usual

    # Add some randomness (±10%)
    random_factor = np.random.uniform(0.9, 1.1)

    return base_multiplier * random_factor


def simulate_current_traffic(G, current_datetime=None):
    """
    Add simulated traffic data to graph edges

    Args:
        G: NetworkX graph
        current_datetime: datetime object (default: now)

    Returns:
        Graph with updated 'current_travel_time' attribute
    """
    if current_datetime is None:
        current_datetime = datetime.now()

    hour = current_datetime.hour
    day_of_week = current_datetime.weekday()

    for u, v, key, data in G.edges(keys=True, data=True):
        road_type = data.get('highway', 'residential')
        base_time = data.get('travel_time', 60)  # seconds

        # Get traffic multiplier
        multiplier = get_traffic_multiplier(road_type, hour, day_of_week)

        # Update travel time
        G[u][v][key]['current_travel_time'] = base_time * multiplier
        G[u][v][key]['traffic_multiplier'] = multiplier

    return G


# Example usage
if __name__ == "__main__":
    import pickle

    # Load network
    with open('../../data/raw/osm/Timişoara_Romania_drive.pkl', 'rb') as f:
        G = pickle.load(f)

    # Simulate traffic for different times
    times = [
        datetime(2024, 2, 5, 8, 0),  # Monday 8 AM (rush hour)
        datetime(2024, 2, 5, 14, 0),  # Monday 2 PM (moderate)
        datetime(2024, 2, 5, 18, 0),  # Monday 6 PM (heavy rush)
        datetime(2024, 2, 10, 15, 0),  # Saturday 3 PM
    ]

    print("=== TRAFFIC SIMULATION EXAMPLES ===")
    for dt in times:
        G = simulate_current_traffic(G, dt)

        # Sample some edges
        sample_edges = list(G.edges(data=True, keys=True))[:5]
        avg_multiplier = np.mean([data['traffic_multiplier'] for _, _, _, data in sample_edges])

        print(f"\n{dt.strftime('%A %I:%M %p')}:")
        print(f"  Average traffic multiplier: {avg_multiplier:.2f}x")