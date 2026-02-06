import osmnx as ox
import pickle
import pandas as pd
import os



def extract_edge_features(G, save_path='../../data/processed/edge_features.csv'):
    """
    Extract all edge attributes into a DataFrame for easy access
    """
    print("Extracting edge features...")

    edges_data = []
    for u, v, key, data in G.edges(keys=True, data=True):
        edge_info = {
            'u': u,
            'v': v,
            'key': key,
            'osmid': data.get('osmid', None),
            'name': data.get('name', 'unnamed'),
            'highway': data.get('highway', 'unknown'),
            'length': data.get('length', 0),
            'speed_kph': data.get('speed_kph', 50),
            'travel_time': data.get('travel_time', 0),
            'lanes': data.get('lanes', None),
            'maxspeed': data.get('maxspeed', None),
            'oneway': data.get('oneway', False),
        }
        edges_data.append(edge_info)

    df = pd.DataFrame(edges_data)

    # Create output directory
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Save to CSV
    df.to_csv(save_path, index=False)
    print(f"Saved {len(df)} edges to {save_path}")

    # Print summary statistics
    print("\n=== EDGE FEATURES SUMMARY ===")
    print(df.describe())

    return df


if __name__ == "__main__":
    # Load network
    G_path = '../../data/raw/osm/Timişoara_Romania_drive.pkl'
    with open(G_path, 'rb') as f:
        G = pickle.load(f)

    # Extract features
    df = extract_edge_features(G)
    print(df.head())
    print("\n✅ Edge features extracted successfully!")