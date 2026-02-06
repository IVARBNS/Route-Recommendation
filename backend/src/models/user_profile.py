import json
import uuid
from datetime import datetime
import os


class UserProfile:
    """Represents a user's preferences and history"""

    def __init__(self, user_id=None, preferences=None, constraints=None):
        self.user_id = user_id or str(uuid.uuid4())
        self.created_at = datetime.now().isoformat()

        # Default preferences (weights sum to 1.0)
        self.preferences = preferences or {
            'time': 0.4,  # Travel time
            'distance': 0.2,  # Route distance
            'safety': 0.15,  # Safety score
            'scenery': 0.15,  # Scenic value
            'simplicity': 0.1  # Fewer turns
        }

        # Constraints
        self.constraints = constraints or {
            'max_time': None,  # Maximum acceptable time (minutes)
            'max_distance': None,  # Maximum distance (km)
            'avoid_highways': False,
            'prefer_bike_lanes': False
        }

        # Route history
        self.history = []

    def add_route_to_history(self, origin, destination, chosen_route, alternatives, context):
        """Record a route choice"""
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'origin': origin,
            'destination': destination,
            'chosen_route': chosen_route,
            'alternatives': alternatives,
            'context': context
        })

    def update_preferences(self, new_preferences):
        """Update preference weights"""
        # Normalize to sum to 1
        total = sum(new_preferences.values())
        self.preferences = {k: v / total for k, v in new_preferences.items()}

    def save(self, filepath):
        """Save profile to JSON file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        data = {
            'user_id': self.user_id,
            'created_at': self.created_at,
            'preferences': self.preferences,
            'constraints': self.constraints,
            'history': self.history
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, filepath):
        """Load profile from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        profile = cls(
            user_id=data['user_id'],
            preferences=data['preferences'],
            constraints=data['constraints']
        )
        profile.created_at = data['created_at']
        profile.history = data['history']

        return profile

    def __repr__(self):
        return f"UserProfile(id={self.user_id[:8]}..., prefs={self.preferences})"


# Example usage
if __name__ == "__main__":
    # Create a user profile
    user = UserProfile()
    print(user)

    # Update preferences
    user.update_preferences({
        'time': 0.5,
        'safety': 0.3,
        'scenery': 0.2
    })
    print(f"Updated preferences: {user.preferences}")

    # Save
    user.save('../../data/processed/user_profiles/user_example.json')
    print("Profile saved!")

    # Load
    loaded_user = UserProfile.load('../../data/processed/user_profiles/user_example.json')
    print(f"Loaded: {loaded_user}")