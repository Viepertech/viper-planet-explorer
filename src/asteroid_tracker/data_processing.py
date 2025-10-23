# data_processing.py
import numpy as np

EARTH_RADIUS_KM = 6371
KM_PER_AU = 149597870.7

def process_neo_data_for_plot(neo_raw_data: dict) -> list:
    asteroids_to_plot = []
    if not neo_raw_data or 'near_earth_objects' not in neo_raw_data:
        print("[data_processing] No 'near_earth_objects' found.")
        return asteroids_to_plot

    rng = np.random.default_rng(12345) 

    for _date, neos in neo_raw_data['near_earth_objects'].items():
        for neo in neos:
            name = neo.get('name', 'Unknown')
            is_hazardous = bool(neo.get('is_potentially_hazardous_asteroid', False))
            estimated_diameter_km = float(
                neo.get('estimated_diameter', {})
                   .get('kilometers', {})
                   .get('estimated_diameter_max', 0.01)
            )

            cad = (neo.get('close_approach_data') or [])
            if not cad:
                continue
            cad0 = cad[0]

            miss_distance_km = float(cad0['miss_distance']['kilometers'])
            relative_velocity_kps = float(cad0['relative_velocity']['kilometers_per_second'])

            miss_distance_au = miss_distance_km / KM_PER_AU
            theta = rng.uniform(0, 2 * np.pi)
            phi = rng.uniform(-np.pi / 2, np.pi / 2)
            x = miss_distance_au * np.cos(phi) * np.cos(theta)
            y = miss_distance_au * np.cos(phi) * np.sin(theta)
            z = miss_distance_au * np.sin(phi)

            asteroids_to_plot.append({
                'name': name,
                'x': x, 'y': y, 'z': z,
                'size': estimated_diameter_km,  
                'is_hazardous': is_hazardous,
                'distance_km': miss_distance_km,
                'velocity_kps': relative_velocity_kps,
                'text': (f"Name: {name}<br>"
                         f"Distance: {miss_distance_km:,.0f} km<br>"
                         f"Velocity: {relative_velocity_kps:.2f} km/s<br>"
                         f"Diameter: {estimated_diameter_km:.3f} km<br>"
                         f"Hazardous: {'Yes' if is_hazardous else 'No'}")
            })

    print(f"[data_processing] Processed {len(asteroids_to_plot)} approach events.")
    return asteroids_to_plot
