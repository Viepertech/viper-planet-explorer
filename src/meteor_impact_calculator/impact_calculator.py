def calculate_kinetic_energy(mass_kg, velocity_kms):
    velocity_ms = velocity_kms * 1000  # Convert to m/s
    return 0.5 * mass_kg * velocity_ms ** 2

def calculate_tnt_equivalent(joules):
    return joules / 4.184e12  # kilotons of TNT

def estimate_crater_diameter(joules):
    # Very rough estimate, valid mostly for rocky surface impacts
    return 0.07 * (joules / 1e9) ** 0.25
