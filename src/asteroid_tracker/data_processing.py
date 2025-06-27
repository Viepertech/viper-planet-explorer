# data_processing.py
import numpy as np

# Constants for Earth's radius in AU
EARTH_RADIUS_KM = 6371
KM_PER_AU = 149597870.7

def process_neo_data_for_plot(neo_raw_data: dict) -> list:
    """
    Processes raw NEO data into a list of dictionaries suitable for 3D plotting.
    Each dictionary contains asteroid properties and simplified 3D coordinates.

    Args:
        neo_raw_data (dict): The raw JSON data from the NeoWs API.

    Returns:
        list: A list of dictionaries, each representing an asteroid event for plotting.
    """
    asteroids_to_plot = []
    if not neo_raw_data or 'near_earth_objects' not in neo_raw_data:
        print("No 'near_earth_objects' found in raw data.")
        return asteroids_to_plot

    for date_str, neos_on_date in neo_raw_data['near_earth_objects'].items():
        for neo in neos_on_date:
            name = neo['name']
            is_hazardous = neo['is_potentially_hazardous_asteroid']
            estimated_diameter_km = neo['estimated_diameter']['kilometers']['estimated_diameter_max']

            # Use the first close approach data for simplicity
            if neo['close_approach_data']:
                cad = neo['close_approach_data'][0]
                miss_distance_km = float(cad['miss_distance']['kilometers'])
                relative_velocity_kps = float(cad['relative_velocity']['kilometers_per_second'])
                # full_approach_date = cad['close_approach_date_full'] # Not used for static plot

                # Convert miss_distance to Astronomical Units
                miss_distance_au = miss_distance_km / KM_PER_AU

                # Simplified 3D position: Random spherical coordinates around Earth
                # This is an approximation for visual spread, not orbital mechanics.
                theta = np.random.uniform(0, 2 * np.pi) # Longitude-like
                phi = np.random.uniform(-np.pi/2, np.pi/2) # Latitude-like

                x = miss_distance_au * np.cos(phi) * np.cos(theta)
                y = miss_distance_au * np.cos(phi) * np.sin(theta)
                z = miss_distance_au * np.sin(phi)

                asteroids_to_plot.append({
                    'name': name,
                    'x': x,
                    'y': y,
                    'z': z,
                    'size': estimated_diameter_km, # Diameter in KM
                    'color': 'red' if is_hazardous else 'blue',
                    'is_hazardous': is_hazardous,
                    'distance_km': miss_distance_km,
                    'velocity_kps': relative_velocity_kps,
                    'text': (f"Name: {name}<br>"
                             f"Distance: {miss_distance_km:.2f} km<br>"
                             f"Velocity: {relative_velocity_kps:.2f} km/s<br>"
                             f"Diameter: {estimated_diameter_km:.2f} km<br>"
                             f"Hazardous: {'Yes' if is_hazardous else 'No'}")
                })
            else:
                # print(f"Warning: Asteroid '{name}' has no close_approach_data.")
                pass # Skip asteroids without close approach data

    print(f"Processed {len(asteroids_to_plot)} close approach events.")
    return asteroids_to_plot

if __name__ == "__main__":
    # Example of how this module processes data (requires dummy raw data)
    dummy_raw_data = {
        "links": {},
        "element_count": 2,
        "near_earth_objects": {
            "2025-06-27": [
                {
                    "name": "Dummy Asteroid 1",
                    "is_potentially_hazardous_asteroid": True,
                    "estimated_diameter": {"kilometers": {"estimated_diameter_max": 0.5}},
                    "close_approach_data": [{"miss_distance": {"kilometers": "1000000"}, "relative_velocity": {"kilometers_per_second": "15.0"}}]
                },
                {
                    "name": "Dummy Asteroid 2",
                    "is_potentially_hazardous_asteroid": False,
                    "estimated_diameter": {"kilometers": {"estimated_diameter_max": 0.05}},
                    "close_approach_data": [{"miss_distance": {"kilometers": "500000"}, "relative_velocity": {"kilometers_per_second": "20.0"}}]
                }
            ]
        }
    }
    processed_data = process_neo_data_for_plot(dummy_raw_data)
    for asteroid in processed_data:
        print(f"Asteroid: {asteroid['name']}, Pos: ({asteroid['x']:.2f}, {asteroid['y']:.2f}, {asteroid['z']:.2f}) AU")
