# visualization.py
import plotly.graph_objects as go
import numpy as np
from typing import List, Dict

EARTH_RADIUS_KM = 6371
KM_PER_AU = 149597870.7
EARTH_RADIUS_AU = EARTH_RADIUS_KM / KM_PER_AU


def create_3d_asteroid_plot(
    asteroids_data: List[Dict],
    title: str = "Near-Earth Asteroids Close Approaches"
) -> go.Figure:
    if not asteroids_data:
        fig = go.Figure()
        fig.update_layout(title="No Asteroid Data Available")
        return fig

    fig = go.Figure()
    u = np.linspace(0, 2 * np.pi, 64)
    v = np.linspace(0, np.pi, 64)
    earth_x = EARTH_RADIUS_AU * np.outer(np.cos(u), np.sin(v))
    earth_y = EARTH_RADIUS_AU * np.outer(np.sin(u), np.sin(v))
    earth_z = EARTH_RADIUS_AU * np.outer(np.ones(np.size(u)), np.cos(v))

    fig.add_trace(go.Surface(
        x=earth_x, y=earth_y, z=earth_z,
        colorscale=[[0, 'rgb(20,70,200)'], [1, 'rgb(0,20,80)']],
        showscale=False, opacity=0.9, name='Earth',
        hoverinfo='name'
    ))

    marker_scaling_factor = 50.0  
    min_px_size = 3.0            

    def to_px(size_km: float) -> float:
        # 'size' is diameter in km in your schema; scale to pixels
        return max(min_px_size, size_km * marker_scaling_factor)

    hazardous = [a for a in asteroids_data if a.get('is_hazardous')]
    nonhaz   = [a for a in asteroids_data if not a.get('is_hazardous')]

    if nonhaz:
        fig.add_trace(go.Scatter3d(
            x=[a['x'] for a in nonhaz],
            y=[a['y'] for a in nonhaz],
            z=[a['z'] for a in nonhaz],
            mode='markers',
            marker=dict(
                size=[to_px(a['size']) for a in nonhaz],
                color='deepskyblue',
                opacity=0.7,
                line=dict(width=0)
            ),
            text=[a.get('text', a.get('name', 'Asteroid')) for a in nonhaz],
            hoverinfo='text',
            name='Asteroids (non-hazardous)'
        ))

    if hazardous:
        fig.add_trace(go.Scatter3d(
            x=[a['x'] for a in hazardous],
            y=[a['y'] for a in hazardous],
            z=[a['z'] for a in hazardous],
            mode='markers',
            marker=dict(
                size=[to_px(a['size']) for a in hazardous],
                color='crimson',
                opacity=0.9,
                line=dict(width=0)
            ),
            text=[a.get('text', a.get('name', 'Asteroid')) for a in hazardous],
            hoverinfo='text',
            name='Asteroids (hazardous)'
        ))

    max_dist_au = max(
        [abs(a['x']) for a in asteroids_data] +
        [abs(a['y']) for a in asteroids_data] +
        [abs(a['z']) for a in asteroids_data]
    )


    plot_limit = max(max_dist_au * 1.2, EARTH_RADIUS_AU * 12)

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X (AU)',
            yaxis_title='Y (AU)',
            zaxis_title='Z (AU)',
            aspectmode='cube',
            xaxis=dict(range=[-plot_limit, plot_limit],
                       showgrid=True, gridcolor="gray",
                       backgroundcolor="black"),
            yaxis=dict(range=[-plot_limit, plot_limit],
                       showgrid=True, gridcolor="gray",
                       backgroundcolor="black"),
            zaxis=dict(range=[-plot_limit, plot_limit],
                       showgrid=True, gridcolor="gray",
                       backgroundcolor="black"),
            bgcolor="black",
        ),
        height=720,
        margin=dict(l=0, r=0, b=0, t=40),
        showlegend=True,
        legend=dict(x=0.02, y=0.98, bgcolor="rgba(0,0,0,0.4)", font=dict(color="white")),
        paper_bgcolor="black",
        font=dict(color="white")
    )

    return fig


def save_spinning_html(
    fig: go.Figure,
    out_path: str = "index.html",
    div_id: str = "plotly-div",
    spin: bool = True,
    rpm: float = 0.6,
    interval_ms: int = 50,
    camera_radius: float = 2.2,
    camera_z: float = 0.5
) -> None:
    """
    Save the Plotly figure to a standalone HTML file and optionally inject
    a small JS loop to auto-rotate (spin) the camera for display on GitHub Pages.

    Args:
        fig: Plotly figure
        out_path: Output HTML path (use 'index.html' for GitHub Pages root)
        div_id: The HTML div id for the plot container
        spin: Enable auto rotation
        rpm: Rotation speed in revolutions per minute
        interval_ms: Animation interval (ms)
        camera_radius: Orbit radius
        camera_z: Camera eye z offset
    """

    html = fig.to_html(
        include_plotlyjs='cdn',
        full_html=True,
        config={"displaylogo": False, "responsive": True},
        div_id=div_id
    )


    style = """
    <style>
      html, body { margin:0; padding:0; background:black; color:white; height:100%; }
      #%(div)s { width:100%%; height:100vh; }
    </style>
    """ % {"div": div_id}

    spin_js = ""
    if spin:
        # angle increment per tick: dθ = 2π * rpm * (interval / 60000)
        spin_js = f"""
<script>
(function() {{
  var angle = 0;
  var div = document.getElementById('{div_id}');
  var interval = {interval_ms};
  var rpm = {rpm};
  var R = {camera_radius};
  var Z = {camera_z};
    injection = style + spin_js
    html = html.replace("</body>", injection + "</body>")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    dummy_processed_data = [
        {'name': 'Test Asteroid 1', 'x': 0.05, 'y': 0.03, 'z': 0.01,
         'size': 0.10, 'is_hazardous': True,  'distance_km': 7_480_000,
         'velocity_kps': 12.5, 'text': 'Test Asteroid 1 — HAZARDOUS'},
        {'name': 'Test Asteroid 2', 'x': -0.02, 'y': 0.04, 'z': -0.03,
         'size': 0.05, 'is_hazardous': False, 'distance_km': 5_980_000,
         'velocity_kps': 18.0, 'text': 'Test Asteroid 2'},
        {'name': 'Test Asteroid 3', 'x': 0.08, 'y': -0.01, 'z': 0.06,
         'size': 0.20, 'is_hazardous': False, 'distance_km': 11_980_000,
         'velocity_kps': 10.0, 'text': 'Test Asteroid 3'}
    ]

    rng = np.random.default_rng(42)
    for i in range(50):
        dist_au = rng.uniform(0.001, 0.1)  
        theta = rng.uniform(0, 2 * np.pi)
        phi = rng.uniform(-np.pi/2, np.pi/2)
        x = dist_au * np.cos(phi) * np.cos(theta)
        y = dist_au * np.cos(phi) * np.sin(theta)
        z = dist_au * np.sin(phi)

        dummy_processed_data.append({
            'name': f'Random Asteroid {i}',
            'x': x, 'y': y, 'z': z,
            'size': float(rng.uniform(0.001, 0.01)),  
            'is_hazardous': False,
            'distance_km': dist_au * KM_PER_AU,
            'velocity_kps': float(rng.uniform(5, 30)),
            'text': f'Random Asteroid {i}'
        })

    fig = create_3d_asteroid_plot(dummy_processed_data, title="Dummy Asteroid Visualization Test")


    save_spinning_html(
        fig,
        out_path="index.html",  
        div_id="plotly-div",
        spin=True,
        rpm=0.6,                
        interval_ms=50,
        camera_radius=2.2,      
        camera_z=0.5            
    )

