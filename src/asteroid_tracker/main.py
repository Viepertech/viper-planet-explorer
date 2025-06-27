# main.py
from datetime import date, timedelta
from api_client import get_neo_feed_data
from data_processing import process_neo_data_for_plot
from visualization import create_3d_asteroid_plot
# from config import NASA_API_KEY # If you need to explicitly pass API key

def run_asteroid_tracker():
    """
    Main function to fetch, process, and visualize NEO data.
    """
    # Define the date range for fetching data
    today = date.today()
    # The NeoWs feed API has a 7-day limit. Let's fetch for the next 7 days.
    start_date = today
    end_date = today + timedelta(days=6) # 7-day range including start_date

    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # 1. Fetch data from NASA API
    neo_raw_data = get_neo_feed_data(start_date_str, end_date_str)

    if neo_raw_data:
        # 2. Process raw data into a plot-friendly format
        asteroids_for_plot = process_neo_data_for_plot(neo_raw_data)

        if asteroids_for_plot:
            # 3. Create and show the 3D visualization
            plot_title = f"Near-Earth Asteroids Close Approaches ({start_date_str} to {end_date_str})"
            fig = create_3d_asteroid_plot(asteroids_for_plot, title=plot_title)
            fig.show()
        else:
            print("No asteroid close approach data found for the specified date range to visualize.")
    else:
        print("Failed to retrieve NEO data from the API. Exiting.")

if __name__ == "__main__":
    run_asteroid_tracker()
