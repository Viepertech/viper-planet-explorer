# visualization.py
import plotly.graph_objects as go
import numpy as np
from typing import List, Dict

EARTH_RADIUS_KM = 6371
KM_PER_AU = 149597870.7
EARTH_RADIUS_AU = EARTH_RADIUS_KM / KM_PER_AU

def create_3d_asteroid_plot(asteroids_data: List[Dict], title: str) -> go.Figure:
    if not asteroids_data:
        fig = go.Figure()
        fig.update_layout(title="No Asteroid Data Available",
                          paper_bgcolor="black", font=dict(color="white"))
        return fig

    fig = go.Figure()

    # Earth sphere
    u = np.linspace(0, 2 * np.pi, 64)
    v = np.linspace(0, np.pi, 64)
    ex = EARTH_RADIUS_AU * np.outer(np.cos(u), np.sin(v))
    ey = EARTH_RADIUS_AU * np.outer(np.sin(u), np.sin(v))
    ez = EARTH_RADIUS_AU * np.outer(np.ones(u.size), np.cos(v))

    fig.add_trace(go.Surface(
        x=ex, y=ey, z=ez,
        colorscale=[[0, 'rgb(20,70,200)'], [1, 'rgb(0,20,80)']],
        showscale=False, opacity=0.9, name='Earth', hoverinfo='name'
    ))

    hazard = [a for a in asteroids_data if a.get('is_hazardous')]
    safe   = [a for a in asteroids_data if not a.get('is_hazardous')]

    def px(size_km: float) -> float:
        return max(3.0, size_km * 50.0)

    if safe:
        fig.add_trace(go.Scatter3d(
            x=[a['x'] for a in safe],
            y=[a['y'] for a in safe],
            z=[a['z'] for a in safe],
            mode='markers',
            marker=dict(size=[px(a['size']) for a in safe],
                        color='deepskyblue', opacity=0.7, line=dict(width=0)),
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
            marker=dict(size=[px(a['size']) for a in hazard],
                        color='crimson', opacity=0.9, line=dict(width=0)),
            text=[a['text'] for a in hazard],
            hoverinfo='text',
            name='Asteroids (hazardous)'
        ))

    max_dist = max(
        [abs(a['x']) for a in asteroids_data] +
        [abs(a['y']) for a in asteroids_data] +
        [abs(a['z']) for a in asteroids_data]
    )
    lim = max(max_dist * 1.2, EARTH_RADIUS_AU * 12)

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X (AU)', yaxis_title='Y (AU)', zaxis_title='Z (AU)',
            aspectmode='cube',
            xaxis=dict(range=[-lim, lim], showgrid=True, gridcolor="gray", backgroundcolor="black"),
            yaxis=dict(range=[-lim, lim], showgrid=True, gridcolor="gray", backgroundcolor="black"),
            zaxis=dict(range=[-lim, lim], showgrid=True, gridcolor="gray", backgroundcolor="black"),
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
    out_path: str = "site/index.html",
    div_id: str = "plotly-div",
    spin: bool = True,
    rpm: float = 0.6,
    interval_ms: int = 50,
    camera_radius: float = 2.2,
    camera_z: float = 0.5
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
    import os
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
