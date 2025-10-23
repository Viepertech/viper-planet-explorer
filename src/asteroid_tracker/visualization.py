# visualization.py
import os
from typing import List, Dict

import numpy as np
import plotly.graph_objects as go

# Units
EARTH_RADIUS_KM = 6371
KM_PER_AU = 149597870.7
EARTH_RADIUS_AU = EARTH_RADIUS_KM / KM_PER_AU


def create_3d_asteroid_plot(
    asteroids_data: List[Dict],
    title: str,
    *,
    earth_scale: float = 50.0,   # visual-only scaling so Earth is visible in AU space
    show_earth_label: bool = True
) -> go.Figure:
    """
    Build a 3D Plotly scene with a solid, Earth-like sphere and asteroid markers.

    asteroids_data items should include:
      x,y,z (in AU); size (km diameter); is_hazardous (bool); text (hover string)
    """
    if not asteroids_data:
        fig = go.Figure()
        fig.update_layout(
            title="No Asteroid Data Available",
            paper_bgcolor="black",
            font=dict(color="white"),
            scene=dict(bgcolor="black"),
        )
        return fig

    fig = go.Figure()

    # ----------------------------
    # Solid Earth sphere (opaque) with Earth-like gradient
    # ----------------------------
    u = np.linspace(0, 2 * np.pi, 160)
    v = np.linspace(0, np.pi, 160)

    r_vis = EARTH_RADIUS_AU * earth_scale
    ex = r_vis * np.outer(np.cos(u), np.sin(v))
    ey = r_vis * np.outer(np.sin(u), np.sin(v))
    ez = r_vis * np.outer(np.ones(u.size), np.cos(v))

    # Use normalized latitude (z/r) for a procedural Earth-like colorscale
    # range will be [-1, 1]; we map it to oceans -> land -> poles
    lat_norm = ez / r_vis

    earth_colorscale = [
        [0.00, "rgb(220, 235, 245)"],  # near south pole (light/icy)
        [0.07, "rgb(0, 40, 100)"],     # deep ocean
        [0.20, "rgb(0, 70, 150)"],     # mid ocean
        [0.35, "rgb(0, 120, 220)"],    # light ocean
        [0.50, "rgb(34, 139, 34)"],    # green land
        [0.65, "rgb(60, 170, 60)"],    # brighter land
        [0.80, "rgb(189, 183, 107)"],  # tan
        [0.93, "rgb(230, 230, 230)"],  # snowy
        [1.00, "rgb(255, 255, 255)"],  # north pole
    ]

    fig.add_trace(go.Surface(
        x=ex, y=ey, z=ez,
        surfacecolor=lat_norm,
        cmin=-1, cmax=1,
        colorscale=earth_colorscale,
        showscale=False,
        opacity=1.0,  # fully opaque / solid
        name="Earth",
        hoverinfo="name",
        lighting=dict(ambient=0.4, diffuse=0.8, specular=0.2, roughness=0.6, fresnel=0.2),
        lightposition=dict(x=1.2, y=1.2, z=0.5),
    ))

    if show_earth_label:
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode='markers+text',
            marker=dict(size=10, color='white'),
            text=["🌍 Earth"],
            textposition="top center",
            name="Earth center",
            hoverinfo="skip"
        ))

    # ----------------------------
    # Asteroids (safe vs hazardous)
    # ----------------------------
    hazard = [a for a in asteroids_data if a.get('is_hazardous')]
    safe   = [a for a in asteroids_data if not a.get('is_hazardous')]

    def px(size_km: float) -> float:
        # enlarge tiny bodies for visibility in AU space
        return max(3.0, float(size_km) * 50.0)

    if safe:
        fig.add_trace(go.Scatter3d(
            x=[a['x'] for a in safe],
            y=[a['y'] for a in safe],
            z=[a['z'] for a in safe],
            mode='markers',
            marker=dict(
                size=[px(a['size']) for a in safe],
                color='deepskyblue',
                opacity=0.8,
                line=dict(width=0)
            ),
            text=[a['text'] for a in safe],
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
            text=[a['text'] for a in hazard],
            hoverinfo='text',
            name='Asteroids (hazardous)'
        ))

    # ----------------------------
    # Scene bounds & styling
    # ----------------------------
    max_dist = max(
        [abs(a['x']) for a in asteroids_data] +
        [abs(a['y']) for a in asteroids_data] +
        [abs(a['z']) for a in asteroids_data]
    )
    lim = max(max_dist * 1.25, r_vis * 6)

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X (AU)', yaxis_title='Y (AU)', zaxis_title='Z (AU)',
            aspectmode='cube',
            xaxis=dict(range=[-lim, lim], showgrid=True, gridcolor="gray", backgroundcolor="black"),
            yaxis=dict(range=[-lim, lim], showgrid=True, gridcolor="gray", backgroundcolor="black"),
            zaxis=dict(range=[-lim, lim], showgrid=True, gridcolor="gray", backgroundcolor="black"),
            bgcolor="black",
            camera=dict(eye=dict(x=2.2, y=0.0, z=0.5))
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
    out_path: str = "site/index.html",
    div_id: str = "plotly-div",
    *,
    spin: bool = True,
    rpm: float = 0.6,
    interval_ms: int = 50,
    camera_radius: float = 2.2,
    camera_z: float = 0.5
) -> None:
    """
    Save a standalone HTML page and (optionally) auto-rotate the camera (great for GitHub Pages).
    """
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

  // Pause auto-rotation briefly if the user manually adjusts the camera
  div.on('plotly_relayout', function() {{
    pausedUntil = Date.now() + 3000;
  }});

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
