from event_fetcher import get_upcoming_events
from calendar_exporter import export_to_ics

def main():
    print("Space Event Calendar Generator")
    events = get_upcoming_events()
    
    print("\nUpcoming Events:")
    for e in events:
        print(f"{e['date']}: {e['name']}")

    export_to_ics(events)

if __name__ == "__main__":
    main()
