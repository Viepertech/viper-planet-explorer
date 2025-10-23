# visualization.py
import os
from typing import List, Dict
import numpy as np
import plotly.graph_objects as go


EARTH_RADIUS_KM = 6371
KM_PER_AU = 149597870.7
EARTH_RADIUS_AU = EARTH_RADIUS_KM / KM_PER_AU


def create_3d_asteroid_plot(
    asteroids_data: List[Dict],
    title: str,
    *,
    earth_min_scale: float = 200.0,    
    earth_fraction_of_range: float = 0.18,  
    show_earth_label: bool = True
) -> go.Figure:
    fig = go.Figure()

    # If no data, still show a nice Earth
    if not asteroids_data:
        asteroids_data = []

    # ----------------------------
    # Determine scene scale from data
    # ----------------------------
    if asteroids_data:
        max_dist = max(
            [abs(a['x']) for a in asteroids_data] +
            [abs(a['y']) for a in asteroids_data] +
            [abs(a['z']) for a in asteroids_data]
        )
    else:
        max_dist = EARTH_RADIUS_AU * earth_min_scale * 4  

    r_vis_from_fraction = max_dist * earth_fraction_of_range
    r_vis_from_min = EARTH_RADIUS_AU * earth_min_scale
    r_vis = max(r_vis_from_fraction, r_vis_from_min)

    lim = max(max_dist * 1.15, r_vis * 2.0)

    u = np.linspace(0, 2 * np.pi, 160)
    v = np.linspace(0, np.pi, 160)
    ex = r_vis * np.outer(np.cos(u), np.sin(v))
    ey = r_vis * np.outer(np.sin(u), np.sin(v))
    ez = r_vis * np.outer(np.ones(u.size), np.cos(v))


    lat_norm = ez / r_vis
    earth_colorscale = [
        [0.00, "rgb(235,240,250)"],  # light ice
        [0.06, "rgb(0, 35, 90)"],    # deep ocean
        [0.22, "rgb(0, 70, 150)"],   # ocean
        [0.40, "rgb(0, 120, 220)"],  # light ocean
        [0.55, "rgb(34, 139, 34)"],  # green land
        [0.72, "rgb(60, 170, 60)"],  # brighter land
        [0.86, "rgb(189,183,107)"],  # tan
        [0.94, "rgb(235,235,235)"],  # snowy
        [1.00, "rgb(255,255,255)"],  # polar cap
    ]

    fig.add_trace(go.Surface(
        x=ex, y=ey, z=ez,
        surfacecolor=lat_norm, cmin=-1, cmax=1,
        colorscale=earth_colorscale,
        showscale=False,
        opacity=1.0,                      
        name="Earth",
        hoverinfo="name",
        lighting=dict(ambient=0.5, diffuse=0.85, specular=0.15, roughness=0.6),
        lightposition=dict(x=1.6, y=1.2, z=0.9),
    ))

    if show_earth_label:
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[r_vis * 1.08],
            mode='text',
            text=["Earth"],
            textposition="middle center",
            name="Earth label",
            hoverinfo="skip",
            showlegend=False
        ))
    hazard = [a for a in asteroids_data if a.get('is_hazardous')]
    safe   = [a for a in asteroids_data if not a.get('is_hazardous')]

    def px(size_km: float) -> float:
        try:
            return max(3.0, float(size_km) * 50.0)
        except Exception:
            return 6.0

    if safe:
        fig.add_trace(go.Scatter3d(
            x=[a['x'] for a in safe],
            y=[a['y'] for a in safe],
            z=[a['z'] for a in safe],
            mode='markers',
            marker=dict(
                size=[px(a['size']) for a in safe],
                color='deepskyblue',
                opacity=0.9,
                line=dict(width=0)
            ),
            text=[a.get('text', a.get('name', 'Asteroid')) for a in safe],
            hoverinfo='text',
            name='Asteroids (non-hazardous)'
        ))

    if hazard:
        fig.add_trace(go.Scatter3d(
            x=[a['x'] for a in hazard],
            y=[a['y'] for a in hazard],
            z=[a['z'] for a in hazard],
            mode='markers',
            marker=dict(
                size=[px(a['size']) for a in hazard],
                color='crimson',
                opacity=0.95,
                line=dict(width=0)
            ),
            text=[a.get('text', a.get('name', 'Asteroid')) for a in hazard],
            hoverinfo='text',
            name='Asteroids (hazardous)'
        ))

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X (AU)', yaxis_title='Y (AU)', zaxis_title='Z (AU)',
            aspectmode='cube',
            xaxis=dict(range=[-lim, lim], showgrid=True, gridcolor="gray", backgroundcolor="black", zeroline=False),
            yaxis=dict(range=[-lim, lim], showgrid=True, gridcolor="gray", backgroundcolor="black", zeroline=False),
            zaxis=dict(range=[-lim, lim], showgrid=True, gridcolor="gray", backgroundcolor="black", zeroline=False),
            bgcolor="black",
            camera=dict(eye=dict(x=2.3, y=0.9, z=0.9))
        ),
        height=720,
        margin=dict(l=0, r=0, b=0, t=48),
        showlegend=True,
        legend=dict(x=0.02, y=0.98, bgcolor="rgba(0,0,0,0.4)", font=dict(color="white")),
        paper_bgcolor="black",
        font=dict(color="white")
    )

    return fig


def save_spinning_html(
    fig: go.Figure,
    out_path: str = "site/index.html",
    div_id: str = "plotly-div",
    *,
    spin: bool = True,
    rpm: float = 0.6,
    interval_ms: int = 50,
    camera_radius: float = 2.6,
    camera_z: float = 0.9
) -> None:
    html = fig.to_html(
        include_plotlyjs='cdn',
        full_html=True,
        config={"displaylogo": False, "responsive": True},
        div_id=div_id
    )

    style = f"""
    <style>
      html, body {{ margin:0; padding:0; background:black; color:white; height:100%; }}
      #{div_id} {{ width:100%; height:100vh; }}
    </style>
    """

    spin_js = ""
    if spin:
        spin_js = f"""
<script>
(function() {{
  var angle = 0;
  var div = document.getElementById('{div_id}');
  var interval = {interval_ms};
  var rpm = {rpm};
  var R = {camera_radius};
  var Z = {camera_z};
  var pausedUntil = 0;
  div.on('plotly_relayout', function() {{ pausedUntil = Date.now() + 3000; }});
  setInterval(function() {{
    if (Date.now() < pausedUntil) return;
    angle += (2*Math.PI) * rpm * (interval/60000.0);
    var cam = {{ eye: {{ x: R*Math.cos(angle), y: R*Math.sin(angle), z: Z }} }};
    Plotly.relayout(div, {{'scene.camera': cam}});
  }}, interval);
}})();
</script>
"""

    html = html.replace("</body>", style + spin_js + "</body>")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
