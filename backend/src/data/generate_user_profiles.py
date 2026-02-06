import numpy as np
import os
from route_recommendation.src.models.user_profile import UserProfile


def generate_diverse_user_profiles(num_users=50, save_dir='../../data/processed/user_profiles'):
    """
    Generate diverse simulated user profiles

    Args:
        num_users: Number of profiles to generate
        save_dir: Directory to save profiles
    """
    os.makedirs(save_dir, exist_ok=True)

    # Define user archetypes
    archetypes = {
        'time_focused': {'time': 0.6, 'distance': 0.2, 'safety': 0.1, 'scenery': 0.05, 'simplicity': 0.05},
        'safety_focused': {'time': 0.2, 'distance': 0.1, 'safety': 0.5, 'scenery': 0.1, 'simplicity': 0.1},
        'scenic_focused': {'time': 0.15, 'distance': 0.15, 'safety': 0.2, 'scenery': 0.4, 'simplicity': 0.1},
        'simple_focused': {'time': 0.2, 'distance': 0.2, 'safety': 0.2, 'scenery': 0.1, 'simplicity': 0.3},
        'balanced': {'time': 0.25, 'distance': 0.2, 'safety': 0.2, 'scenery': 0.2, 'simplicity': 0.15},
    }

    profiles = []

    for i in range(num_users):
        # Select archetype
        archetype_name = np.random.choice(list(archetypes.keys()))
        base_prefs = archetypes[archetype_name].copy()

        # Add some random variation (±20%)
        for key in base_prefs:
            variation = np.random.uniform(-0.2, 0.2)
            base_prefs[key] = max(0.01, base_prefs[key] * (1 + variation))

        # Normalize
        total = sum(base_prefs.values())
        prefs = {k: v / total for k, v in base_prefs.items()}

        # Create profile
        user = UserProfile(preferences=prefs)
        user.archetype = archetype_name  # Add for reference

        # Save
        filepath = os.path.join(save_dir, f'user_{i:03d}.json')
        user.save(filepath)

        profiles.append(user)

        if (i + 1) % 10 == 0:
            print(f"Generated {i + 1} profiles...")

    print(f"\n✅ Generated {num_users} user profiles!")
    print(f"Saved to: {save_dir}/")

    # Print summary
    print("\n=== PROFILE DISTRIBUTION ===")
    for archetype in archetypes.keys():
        count = sum(1 for p in profiles if p.archetype == archetype)
        print(f"{archetype}: {count}")

    return profiles


if __name__ == "__main__":
    generate_diverse_user_profiles(num_users=50)