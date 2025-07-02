from datetime import datetime
from planetary_time import get_planetary_time, PLANET_DAY_LENGTHS

def print_planet_menu():
    print("\nSelect a planet to convert time:")
    for i, planet in enumerate(PLANET_DAY_LENGTHS.keys()):
        print(f"{i + 1}. {planet}")
    print("0. Exit")

def main():
    print("Welcome to the Planetary Time Converter!")
    while True:
        earth_time = datetime.utcnow()
        print(f"\nCurrent Earth Time (UTC): {earth_time.strftime('%H:%M:%S')}")

        print_planet_menu()
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 0:
            print("Goodbye, space traveler!")
            break

        planets = list(PLANET_DAY_LENGTHS.keys())
        if 1 <= choice <= len(planets):
            planet = planets[choice - 1]
            converted = get_planetary_time(earth_time, planet)
            print(f"Time on {planet}: {converted}")
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
