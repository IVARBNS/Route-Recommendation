import osmnx as ox
import geopandas as gpd
import pandas as pd
import os


def download_pois(place_name, tags, save_dir='../../data/raw/pois'):
    """
    Download Points of Interest from OpenStreetMap

    Args:
        place_name: Name of place (e.g., "Bucharest, Romania")
        tags: Dictionary of OSM tags to query
        save_dir: Directory to save POI data

    Returns:
        GeoDataFrame with POIs
    """
    os.makedirs(save_dir, exist_ok=True)

    all_pois = []

    for category, tag_dict in tags.items():
        print(f"Downloading {category}...")
        try:
            pois = ox.features_from_place(place_name, tag_dict)
            pois['category'] = category
            all_pois.append(pois)
            print(f"  Found {len(pois)} {category}")
        except Exception as e:
            print(f"  Error downloading {category}: {e}")

    if not all_pois:
        print("No POIs downloaded!")
        return None

    # Combine all POIs
    combined_pois = gpd.GeoDataFrame(pd.concat(all_pois, ignore_index=True))

    # Keep only point geometries (some POIs are polygons)
    combined_pois = combined_pois[combined_pois.geometry.type == 'Point']

    # Clean column names - replace problematic characters
    combined_pois.columns = combined_pois.columns.str.replace(':', '_', regex=False)
    combined_pois.columns = combined_pois.columns.str.replace('@', '_', regex=False)

    # Save to file
    output_path = os.path.join(save_dir, f"{place_name.replace(' ', '_').replace(',', '')}_pois.gpkg")
    combined_pois.to_file(output_path, driver='GPKG')
    print(f"\nSaved {len(combined_pois)} POIs to {output_path}")

    # Also save as CSV for easy viewing
    csv_path = output_path.replace('.gpkg', '.csv')
    poi_df = combined_pois.copy()
    poi_df['lat'] = poi_df.geometry.y
    poi_df['lon'] = poi_df.geometry.x
    poi_df.drop(columns=['geometry']).to_csv(csv_path, index=False)
    print(f"Also saved to {csv_path}")

    return combined_pois


if __name__ == "__main__":
    CITY_NAME = "Timişoara, Romania"  # CHANGE THIS

    # Define POI categories to download
    POI_TAGS = {
        'parks': {'leisure': 'park'},
        'water': {'natural': ['water', 'waterway']},
        'restaurants': {'amenity': 'restaurant'},
        'cafes': {'amenity': 'cafe'},
        'gas_stations': {'amenity': 'fuel'},
        'parking': {'amenity': 'parking'},
        'hospitals': {'amenity': 'hospital'},
        'police': {'amenity': 'police'},
        'schools': {'amenity': 'school'},
        'banks': {'amenity': 'bank'},
        'pharmacies': {'amenity': 'pharmacy'},
        'historic': {'historic': True},
        'tourism': {'tourism': ['attraction', 'museum', 'viewpoint']},
    }

    # Download POIs
    pois = download_pois(CITY_NAME, POI_TAGS)

    if pois is not None:
        print("\n=== POI SUMMARY ===")
        print(pois.groupby('category').size().sort_values(ascending=False))
        print("\n✅ POIs downloaded successfully!")