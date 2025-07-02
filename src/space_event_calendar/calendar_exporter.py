from ics import Calendar, Event

def export_to_ics(events, filename="space_events.ics"):
    calendar = Calendar()
    for e in events:
        event = Event()
        event.name = e["name"]
        event.begin = e["date"]
        event.description = f"Astronomy event: {e['name']}"
        calendar.events.add(event)
    with open(filename, "w") as f:
        f.writelines(calendar)
    print(f"Calendar exported to {filename}")
