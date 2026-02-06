import pickle
import os
from download_osm import download_city_network, load_network
from download_pois import download_pois
from generate_user_profiles import generate_diverse_user_profiles
from simulate_traffic import simulate_current_traffic
import geopandas as gpd


def build_complete_dataset(city_name="Timişoara, Romania"):
    """
    Complete data pipeline - downloads and processes all data sources
    """
    print("=" * 60)
    print("BUILDING COMPLETE DATASET FOR ROUTE RECOMMENDATION")
    print("=" * 60)

    # Step 1: Road Network
    print("\n[1/4] Downloading road network...")
    network_path = f'../../data/raw/osm/{city_name.replace(" ", "_").replace(",", "")}_drive.pkl'

    if os.path.exists(network_path):
        print(f"  Loading existing network from {network_path}")
        G = load_network(network_path)
    else:
        G = download_city_network(city_name, 'drive')

    print(f"  ✓ Network: {G.number_of_nodes():,} nodes, {G.number_of_edges():,} edges")

    # Step 2: POIs
    print("\n[2/4] Downloading Points of Interest...")
    poi_path = f'../../data/raw/pois/{city_name.replace(" ", "_").replace(",", "")}_pois.gpkg'

    if os.path.exists(poi_path):
        print(f"  Loading existing POIs from {poi_path}")
        pois = gpd.read_file(poi_path)
    else:
        POI_TAGS = {
            'parks': {'leisure': 'park'},
            'restaurants': {'amenity': 'restaurant'},
            'gas_stations': {'amenity': 'fuel'},
            'hospitals': {'amenity': 'hospital'},
            'historic': {'historic': True},
        }
        pois = download_pois(city_name, POI_TAGS)

    print(f"  ✓ POIs: {len(pois):,} points across {pois['category'].nunique()} categories")

    # Step 3: User Profiles
    print("\n[3/4] Generating user profiles...")
    profile_dir = '../../data/processed/user_profiles'

    if os.path.exists(profile_dir) and len(os.listdir(profile_dir)) > 0:
        print(f"  User profiles already exist in {profile_dir}")
        num_profiles = len([f for f in os.listdir(profile_dir) if f.endswith('.json')])
        print(f"  ✓ Found {num_profiles} existing profiles")
    else:
        generate_diverse_user_profiles(num_users=50)
        print(f"  ✓ Generated 50 user profiles")

    # Step 4: Add simulated traffic
    print("\n[4/4] Adding simulated traffic data...")
    G = simulate_current_traffic(G)

    # Save updated network
    updated_path = network_path.replace('.pkl', '_with_traffic.pkl')
    with open(updated_path, 'wb') as f:
        pickle.dump(G, f)
    print(f"  ✓ Saved network with traffic to {updated_path}")

    # Summary
    print("\n" + "=" * 60)
    print("✅ DATASET COMPLETE!")
    print("=" * 60)
    print(f"\nData locations:")
    print(f"  Road network: {network_path}")
    print(f"  Network + traffic: {updated_path}")
    print(f"  POIs: {poi_path}")
    print(f"  User profiles: {profile_dir}/")
    print(f"\nYou can now proceed to route generation and recommendation!")

    return G, pois


if __name__ == "__main__":
    G, pois = build_complete_dataset("Timişoara, Romania")