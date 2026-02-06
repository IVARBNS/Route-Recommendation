import osmnx as ox
import networkx as nx
import pickle
import os

CITY_DATA_PATH_OSM = "../../data/raw/osm/"

def download_city_network(city_name, network_type='drive', save_dir=CITY_DATA_PATH_OSM):
    """
    Download road network from OpenStreetMap

    Args:
        city_name: Name of city (e.g., "Bucharest, Romania")
        network_type: 'drive', 'walk', 'bike', or 'all'
        save_dir: Directory to save the data

    Returns:
        NetworkX MultiDiGraph
    """
    print(f"Downloading {network_type} network for {city_name}...")

    # Create save directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    # Download the network
    # This might take 2-10 minutes depending on city size
    G = ox.graph_from_place(city_name, network_type=network_type)

    print(f"Downloaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

    # Add additional attributes
    print("Adding speed and travel time information...")
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)

    # Save in multiple formats
    print("Saving graph...")

    # GraphML format (human-readable, preserves attributes)
    graphml_path = os.path.join(save_dir, f"{city_name.replace(' ', '_').replace(',', '')}_{network_type}.graphml")
    ox.save_graphml(G, graphml_path)
    print(f"Saved GraphML to {graphml_path}")

    # Pickle format (fastest to load)
    pickle_path = os.path.join(save_dir, f"{city_name.replace(' ', '_').replace(',', '')}_{network_type}.pkl")
    with open(pickle_path, 'wb') as f:
        pickle.dump(G, f)
    print(f"Saved pickle to {pickle_path}")

    # GeoPackage format (for GIS software)
    gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
    gpkg_path = os.path.join(save_dir, f"{city_name.replace(' ', '_').replace(',', '')}_{network_type}.gpkg")
    gdf_nodes.to_file(gpkg_path, layer='nodes', driver='GPKG')
    gdf_edges.to_file(gpkg_path, layer='edges', driver='GPKG')
    print(f"Saved GeoPackage to {gpkg_path}")

    return G


def load_network(filepath):
    """
    Load a previously saved network

    Args:
        filepath: Path to .pkl or .graphml file
    """
    if filepath.endswith('.pkl'):
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    elif filepath.endswith('.graphml'):
        return ox.load_graphml(filepath)
    else:
        raise ValueError("File must be .pkl or .graphml")


def get_network_statistics(G):
    """Print useful statistics about the network"""
    print("\n=== NETWORK STATISTICS ===")
    print(f"Number of nodes: {G.number_of_nodes():,}")
    print(f"Number of edges: {G.number_of_edges():,}")

    # Get edge attributes
    edge_attrs = set()
    for u, v, data in G.edges(data=True):
        edge_attrs.update(data.keys())
        break  # Just check first edge
    print(f"\nAvailable edge attributes: {edge_attrs}")

    # Count road types
    from collections import Counter
    highway_types = []
    for u, v, data in G.edges(data=True):
        highway = data.get('highway', 'unknown')
        if isinstance(highway, list):
            highway_types.extend(highway)
        else:
            highway_types.append(highway)

    print("\nRoad type distribution:")
    for road_type, count in Counter(highway_types).most_common(10):
        print(f"  {road_type}: {count:,}")

    return G


if __name__ == "__main__":
    # Configuration
    CITY_NAME = "Timişoara, Romania"  # CHANGE THIS to your city
    NETWORK_TYPE = "drive"  # drive, walk, bike, or all

    # Download the network
    G = download_city_network(CITY_NAME, NETWORK_TYPE)

    # Print statistics
    get_network_statistics(G)

    print("\n✅ Road network downloaded successfully!")
    print(f"Files saved in: backend/data/raw/osm/")