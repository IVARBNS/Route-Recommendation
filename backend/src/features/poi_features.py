import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point, LineString
from scipy.spatial import cKDTree


def calculate_poi_proximity(route_geometry, pois_gdf, category=None, max_distance=500):
    """
    Calculate proximity of route to POIs

    Args:
        route_geometry: LineString or list of (lat, lon) tuples
        pois_gdf: GeoDataFrame with POIs
        category: Filter POIs by category (optional)
        max_distance: Maximum distance to consider (meters)

    Returns:
        Dictionary with proximity metrics
    """
    # Filter by category if specified
    if category:
        pois = pois_gdf[pois_gdf['category'] == category].copy()
    else:
        pois = pois_gdf.copy()

    if len(pois) == 0:
        return {
            'min_distance': np.inf,
            'avg_distance': np.inf,
            'count_within_range': 0,
            'proximity_score': 0
        }

    # Convert route to LineString if needed
    if isinstance(route_geometry, list):
        route_line = LineString([(lon, lat) for lat, lon in route_geometry])
    else:
        route_line = route_geometry

    # Convert to projected CRS (UTM zone 35N for Romania)
    # First, create a GeoSeries for the route
    route_gs = gpd.GeoSeries([route_line], crs='EPSG:4326')

    # Reproject both to UTM (meters)
    pois_projected = pois.to_crs('EPSG:32635')  # UTM zone 35N
    route_projected = route_gs.to_crs('EPSG:32635')

    # Calculate distances (now in meters)
    distances = pois_projected.geometry.distance(route_projected.iloc[0])

    # Calculate metrics
    min_dist = distances.min()
    avg_dist = distances.mean()
    count_within = (distances <= max_distance).sum()

    # Proximity score (higher is better)
    # 1.0 if POI is right on route, 0.0 if beyond max_distance
    proximity_score = max(0, 1 - (min_dist / max_distance))

    return {
        'min_distance': min_dist,
        'avg_distance': avg_dist,
        'count_within_range': count_within,
        'proximity_score': proximity_score
    }


def add_poi_features_to_routes(routes_df, pois_gdf):
    """
    Add POI-based features to a DataFrame of routes

    Args:
        routes_df: DataFrame with 'geometry' column (LineString)
        pois_gdf: GeoDataFrame with POIs

    Returns:
        DataFrame with added POI features
    """
    categories = pois_gdf['category'].unique()

    for category in categories:
        print(f"Processing {category}...")

        feature_name = f'poi_{category}'
        routes_df[f'{feature_name}_proximity'] = routes_df['geometry'].apply(
            lambda geom: calculate_poi_proximity(geom, pois_gdf, category)['proximity_score']
        )
        routes_df[f'{feature_name}_count'] = routes_df['geometry'].apply(
            lambda geom: calculate_poi_proximity(geom, pois_gdf, category)['count_within_range']
        )

    return routes_df


# Example usage
if __name__ == "__main__":
    # Load POIs
    pois = gpd.read_file('../../data/raw/pois/Timişoara_Romania_pois.gpkg')

    # Test with a sample route
    sample_route = LineString([
        (21.2272, 45.7489),  # Victory Square
        (21.2297, 45.7537),  # Bega River area
        (21.2350, 45.7560),  # Cathedral area
        (21.2400, 45.7580),  # Towards Fabric district
    ])

    # Calculate proximity to parks
    park_proximity = calculate_poi_proximity(sample_route, pois, category='parks')
    print("Park proximity metrics:", park_proximity)