import pickle
import geopandas as gpd
import os
import json


def test_all_data_sources():
    """Verify all data sources are accessible"""

    print("Testing data sources...\n")

    # Test 1: Road Network
    print("[1] Testing road network...")
    try:
        with open(
            "route_recommendation/data/raw/osm/Timişoara_Romania_drive.pkl", "rb"
        ) as f:
            G = pickle.load(f)
        print(f"  ✓ Loaded graph: {G.number_of_nodes():,} nodes")

        # Check for required attributes
        sample_edge = list(G.edges(data=True))[0]
        required_attrs = ["length", "speed_kph", "travel_time"]
        for attr in required_attrs:
            assert attr in sample_edge[2], f"Missing {attr}"
        print(f"  ✓ Has required attributes: {required_attrs}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

    # Test 2: POIs
    print("\n[2] Testing POIs...")
    try:
        pois = gpd.read_file(
            "route_recommendation/data/raw/pois/Timişoara_Romania_pois.gpkg"
        )
        print(f"  ✓ Loaded {len(pois):,} POIs")
        print(f"  ✓ Categories: {list(pois['category'].unique())}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

    # Test 3: User Profiles
    print("\n[3] Testing user profiles...")
    try:
        profile_dir = "route_recommendation/data/processed/user_profiles"
        profiles = [f for f in os.listdir(profile_dir) if f.endswith(".json")]
        print(f"  ✓ Found {len(profiles)} user profiles")

        # Load one profile
        with open(os.path.join(profile_dir, profiles[0]), "r") as f:
            sample_profile = json.load(f)
        print(f"  ✓ Sample preferences: {sample_profile['preferences']}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

    # Test 4: Traffic Data
    print("\n[4] Testing traffic simulation...")
    try:
        with open(
            "route_recommendation/data/raw/osm/Timişoara_Romania_drive_with_traffic.pkl",
            "rb",
        ) as f:
            G_traffic = pickle.load(f)

        sample_edge = list(G_traffic.edges(data=True))[0]
        assert "current_travel_time" in sample_edge[2], "Missing traffic data"
        print(f"  ✓ Traffic data available")
        print(
            f"  ✓ Sample traffic multiplier: {sample_edge[2].get('traffic_multiplier', 1.0):.2f}x"
        )
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

    print("\n" + "=" * 50)
    print("✅ ALL DATA SOURCES VERIFIED!")
    print("=" * 50)
    return True


if __name__ == "__main__":
    test_all_data_sources()
