# ☄️ Near-Earth Asteroid 3D Tracker

> 🌐 **Live Visualization:**  
> [View the Interactive Demo](https://viepertech.github.io/viper-planet-explorer//)

## 🛰️ Overview

This project visualizes **Near-Earth Objects (NEOs)** using live data from NASA’s [NeoWs (Near Earth Object Web Service)](https://api.nasa.gov/).  
It generates a **3D interactive scene** showing asteroid flybys near Earth, highlighting which are potentially hazardous.

Each asteroid is plotted in **Astronomical Units (AU)**, scaled in size, and color-coded by hazard level:

- 🟦 **Blue:** Non-hazardous asteroids  
- 🟥 **Red:** Potentially hazardous asteroids  
- 🌍 **Green–Blue Earth:** Scaled-up solid Earth sphere at the origin  

## How to Run Locally

Clone the repo and run it with Python:

```
git clone https://github.com/Viepertech/viper-planet-explorer.git
cd viper-planet-explorer
pip install -r requirements.txt
```

> Optional: set your NASA API key (get one free from https://api.nasa.gov)

`export NASA_API_KEY="your_key_here"`

`cd src && python -m asteroid_tracker.main`


## File Structure 

```
viper-planet-explorer/
├── requirements.txt
├── .github/
│   └── workflows/
│       └── pages.yml          # Deploys to GitHub Pages
└── src/
    └── asteroid_tracker/
        ├── api_client.py      # Fetches asteroid data from NASA
        ├── config.py          # Holds API key and base URL
        ├── data_processing.py # Turns raw data into coordinates
        ├── visualization.py   # Draws Earth, asteroids, and rotation
        └── main.py            # Runs everything and saves index.html
```

## 🌍 How It Works

1. **`api_client.py`** — Fetches asteroid data from NASA’s API.
2. **`data_processing.py`** — Processes and scales asteroid positions for 3D plotting.
3. **`visualization.py`** — Builds a high-quality **solid Earth** model and plots all asteroids.
4. **`main.py`** — Orchestrates the whole pipeline and saves a standalone `index.html`.
5. **GitHub Actions (`.github/workflows/pages.yml`)** — Automatically:
   - Installs dependencies  
   - Runs the script to fetch new data  
   - Publishes `site/index.html` to **GitHub Pages**

## 🧩 Features

✅ **Solid, opaque Earth** with realistic gradient  
✅ **Spinning 3D camera** for cinematic visualization  
✅ **NASA live data refresh** on every workflow run  
✅ **Standalone HTML** (no backend needed)  
✅ **Fully automated GitHub Pages deployment**

## 🧠 Technical Details

- **Data Source:** [NASA NeoWs API](https://api.nasa.gov/)  
- **Visualization:** Plotly 3D (`plotly.graph_objects`)  
- **Languages:** Python 3.11+, NumPy, Plotly  
- **Deployed With:** GitHub Actions → GitHub Pages  

### Code Entry Point
```bash
cd src
python -m asteroid_tracker.main
