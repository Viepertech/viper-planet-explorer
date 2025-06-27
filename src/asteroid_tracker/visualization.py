# visualization.py
import plotly.graph_objects as go
import numpy as np

# Constants for Earth's radius in AU (matching data_processing.py)
EARTH_RADIUS_KM = 6371
KM_PER_AU = 149597870.7
EARTH_RADIUS_AU = EARTH_RADIUS_KM / KM_PER_AU


def create_3d_asteroid_plot(asteroids_data: list, title: str = "Near-Earth Asteroids Close Approaches") -> go.Figure:
    """
    Creates an interactive 3D Plotly figure showing Earth and asteroids.

    Args:
        asteroids_data (list): A list of dictionaries, each representing an asteroid event,
                                as prepared by process_neo_data_for_plot.
        title (str): The title for the plot.

    Returns:
        go.Figure: A Plotly Figure object.
    """
    if not asteroids_data:
        print("No asteroid data provided for visualization.")
        fig = go.Figure()
        fig.update_layout(title="No Asteroid Data Available")
        return fig

    fig = go.Figure()

    # Add Earth Sphere
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    earth_x = EARTH_RADIUS_AU * np.outer(np.cos(u), np.sin(v))
    earth_y = EARTH_RADIUS_AU * np.outer(np.sin(u), np.sin(v))
    earth_z = EARTH_RADIUS_AU * np.outer(np.ones(np.size(u)), np.cos(v))

    fig.add_trace(go.Surface(
        x=earth_x, y=earth_y, z=earth_z,
        colorscale=[[0, 'blue'], [1, 'darkblue']],
        showscale=False, opacity=0.8, name='Earth',
        hoverinfo='name'
    ))

    # Add Asteroids
    asteroid_x = [a['x'] for a in asteroids_data]
    asteroid_y = [a['y'] for a in asteroids_data]
    asteroid_z = [a['z'] for a in asteroids_data]
    
    # Scale marker size based on asteroid's actual diameter for visual effect
    # You might need to adjust this scaling factor for better visibility
    # For example, 1 unit on the plot might represent 1 AU.
    # Asteroids are tiny compared to AU, so we scale them up considerably.
    # A diameter of 1km might be represented by a marker size of, say, 10-20.
    marker_scaling_factor = 50 # Adjust this value!
    asteroid_marker_sizes = [a['size'] * marker_scaling_factor for a in asteroids_data]
    
    asteroid_colors = ['red' if a['is_hazardous'] else 'blue' for a in asteroids_data]
    asteroid_text = [a['text'] for a in asteroids_data]

    fig.add_trace(go.Scatter3d(
        x=asteroid_x,
        y=asteroid_y,
        z=asteroid_z,
        mode='markers',
        marker=dict(
            size=asteroid_marker_sizes,
            color=asteroid_colors,
            opacity=0.7,
            line=dict(width=0) # No border for markers
        ),
        text=asteroid_text,
        hoverinfo='text',
        name='Asteroids'
    ))

    # Set up the scene layout
    # Calculate a sensible range for the axes based on asteroid distances
    max_dist_au = max([abs(a['x']) for a in asteroids_data] +
                      [abs(a['y']) for a in asteroids_data] +
                      [abs(a['z']) for a in asteroids_data])
    
    # Add some padding to the limits
    plot_limit = max_dist_au * 1.2 if max_dist_au > EARTH_RADIUS_AU * 2 else EARTH_RADIUS_AU * 10
    
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X (AU)',
            yaxis_title='Y (AU)',
            zaxis_title='Z (AU)',
            aspectmode='cube', # Ensures equal scaling on all axes for proper perspective
            xaxis=dict(range=[-plot_limit, plot_limit]),
            yaxis=dict(range=[-plot_limit, plot_limit]),
            zaxis=dict(range=[-plot_limit, plot_limit]),
            # Optional: background colors
            bgcolor="black",
            xaxis_backgroundcolor="black",
            yaxis_backgroundcolor="black",
            zaxis_backgroundcolor="black",
            # Optional: grid lines
            xaxis_showgrid=True,
            yaxis_showgrid=True,
            zaxis_showgrid=True,
            gridcolor="gray",
        ),
        height=700, # Adjust figure height
        margin=dict(l=0, r=0, b=0, t=40), # Adjust margins
        showlegend=True,
        hovermode="closest",
        legend=dict(x=0, y=1, traceorder="normal", bgcolor="rgba(255,255,255,0.7)"),
    )

    return fig

if __name__ == "__main__":
    # Example usage for testing this module (requires dummy processed data)
    dummy_processed_data = [
        {'name': 'Test Asteroid 1', 'x': 0.05, 'y': 0.03, 'z': 0.01, 'size': 0.1, 'is_hazardous': True, 'distance_km': 7480000, 'velocity_kps': 12.5, 'text': '...'},
        {'name': 'Test Asteroid 2', 'x': -0.02, 'y': 0.04, 'z': -0.03, 'size': 0.05, 'is_hazardous': False, 'distance_km': 5980000, 'velocity_kps': 18.0, 'text': '...'},
        {'name': 'Test Asteroid 3', 'x': 0.08, 'y': -0.01, 'z': 0.06, 'size': 0.2, 'is_hazardous': False, 'distance_km': 11980000, 'velocity_kps': 10.0, 'text': '...'}
    ]
    
    # Generate random positions for more asteroids to see density
    for _ in range(50): # Add 50 more random non-hazardous asteroids
        dist_au = np.random.uniform(0.001, 0.1) # Between ~150k km and ~15M km
        theta = np.random.uniform(0, 2 * np.pi)
        phi = np.random.uniform(-np.pi/2, np.pi/2)
        x = dist_au * np.cos(phi) * np.cos(theta)
        y = dist_au * np.cos(phi) * np.sin(theta)
        z = dist_au * np.sin(phi)
        
        dummy_processed_data.append({
            'name': f'Random Asteroid {_}',
            'x': x, 'y': y, 'z': z,
            'size': np.random.uniform(0.001, 0.01), # Small diameter
            'is_hazardous': False,
            'distance_km': dist_au * KM_PER_AU,
            'velocity_kps': np.random.uniform(5, 30),
            'text': f'Random Asteroid {_}'
        })

    fig = create_3d_asteroid_plot(dummy_processed_data, title="Dummy Asteroid Visualization Test")
    fig.show()
