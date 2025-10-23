# main.py
from datetime import date, timedelta
from .api_client import get_neo_feed_data
from .data_processing import process_neo_data_for_plot
from .visualization import create_3d_asteroid_plot, save_spinning_html

def run_asteroid_tracker():
    today = date.today()
    start_date = today
    end_date = today + timedelta(days=6) 
    s = start_date.strftime("%Y-%m-%d")
    e = end_date.strftime("%Y-%m-%d")

    neo_raw = get_neo_feed_data(s, e)
    if not neo_raw:
        print("[main] API failed; producing an empty page.")
        fig = create_3d_asteroid_plot([], title=f"Near-Earth Asteroids ({s} → {e})")
        save_spinning_html(fig, out_path="site/index.html")
        return

    asteroids = process_neo_data_for_plot(neo_raw)
    title = f"Near-Earth Asteroids Close Approaches ({s} → {e})"
    fig = create_3d_asteroid_plot(asteroids, title=title)
    save_spinning_html(fig, out_path="site/index.html")

if __name__ == "__main__":
    run_asteroid_tracker()
