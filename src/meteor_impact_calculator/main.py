from impact_calculator import calculate_kinetic_energy, calculate_tnt_equivalent, estimate_crater_diameter

def main():
    print("Meteor Impact Energy Calculator")

    try:
        mass = float(input("Enter mass of meteor (in kg): "))
        velocity = float(input("Enter velocity (in km/s): "))

        energy = calculate_kinetic_energy(mass, velocity)
        tnt = calculate_tnt_equivalent(energy)
        crater = estimate_crater_diameter(energy)

        print(f"\nEstimated Kinetic Energy: {energy:.2e} J")
        print(f"Equivalent to ~{tnt:.2f} kilotons of TNT")
        print(f"Estimated crater diameter: {crater:.2f} meters")

    except ValueError:
        print("Invalid input. Please enter numbers only.")

if __name__ == "__main__":
    main()
