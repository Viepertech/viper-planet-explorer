from datetime import datetime

# Planet rotation periods in Earth hours
PLANET_DAY_LENGTHS = {
    "Mercury": 1407.6,
    "Venus": -5832.5,
    "Earth": 24.0,
    "Mars": 24.6,
    "Jupiter": 9.9,
    "Saturn": 10.7,
    "Uranus": -17.2,
    "Neptune": 16.1
}

def get_planetary_time(earth_time: datetime, planet: str) -> str:
    if planet not in PLANET_DAY_LENGTHS:
        raise ValueError(f"Unknown planet: {planet}")

    planet_day = PLANET_DAY_LENGTHS[planet]
    is_retrograde = planet_day < 0
    planet_day = abs(planet_day)

    # Fraction of Earth day passed
    seconds_since_midnight = (
        earth_time - earth_time.replace(hour=0, minute=0, second=0, microsecond=0)
    ).total_seconds()
    fraction_of_day = seconds_since_midnight / (24 * 3600)

    # Convert to planet time
    planetary_seconds = fraction_of_day * planet_day * 3600
    planetary_hours = int(planetary_seconds // 3600) % int(planet_day)
    planetary_minutes = int((planetary_seconds % 3600) // 60)

    if is_retrograde:
        planetary_hours = int(planet_day) - planetary_hours

    return f"{planetary_hours:02d}:{planetary_minutes:02d} (Local {planet} Time)"
