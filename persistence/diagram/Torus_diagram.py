
import plotly.graph_objects as go

# Torus filtration data (time, dim, vertices)
input_data = [
    (2, 2, [1, 2, 4]), (2, 2, [2, 4, 5]), (2, 2, [2, 3, 5]), (2, 2, [3, 5, 6]), (2, 2, [1, 3, 6]),
    (2, 2, [1, 4, 6]), (2, 2, [4, 5, 7]), (2, 2, [5, 7, 8]), (2, 2, [5, 6, 8]), (2, 2, [6, 8, 9]),
    (2, 2, [4, 6, 9]), (2, 2, [4, 7, 9]), (2, 2, [1, 7, 8]), (2, 2, [1, 2, 8]), (2, 2, [2, 8, 9]),
    (2, 2, [2, 3, 9]), (2, 2, [3, 7, 9]), (2, 2, [1, 3, 7]), (1, 1, [2, 4]), (1, 1, [1, 4]), 
    (1, 1, [1, 2]), (1, 1, [4, 5]), (1, 1, [2, 5]), (1, 1, [3, 5]), (1, 1, [2, 3]), (1, 1, [5, 6]),
    (1, 1, [3, 6]), (1, 1, [1, 6]), (1, 1, [1, 3]), (1, 1, [4, 6]), (1, 1, [5, 7]), (1, 1, [4, 7]),
    (1, 1, [7, 8]), (1, 1, [5, 8]), (1, 1, [6, 8]), (1, 1, [8, 9]), (1, 1, [6, 9]), (1, 1, [4, 9]),
    (1, 1, [7, 9]), (1, 1, [1, 8]), (1, 1, [1, 7]), (1, 1, [2, 8]), (1, 1, [2, 9]), (1, 1, [3, 9]),
    (1, 1, [3, 7]), (0, 0, [4]), (0, 0, [2]), (0, 0, [1]), (0, 0, [5]), (0, 0, [3]), (0, 0, [6]),
    (0, 0, [7]), (0, 0, [8]), (0, 0, [9])
]

# 3D positions of vertices on a torus (approximation for visualization)
vertex_positions = {
    1: [1, 0, 0],
    2: [0.5, 0.87, 0.5],
    3: [-0.5, 0.87, -0.5],
    4: [-1, 0, 0],
    5: [-0.5, -0.87, 0.5],
    6: [0.5, -0.87, -0.5],
    7: [1.5, 0, 0],
    8: [0.5, 1.87, 0.5],
    9: [-1.5, 0, -0.5]
}

# Function to create interactive 3D plots for each time instance
def plot_simplices_3d_instances(input_data):
    ''' 
        Input: list of (time, dim, vertices)
        Example: [(2, 2, [1, 2, 4]), (1, 1, [2, 4]), (0, 0, [4])]
        
        Output: 3D plot for the simplices at every time instance
    '''
    # Group data by time instances
    time_instances = {}
    for dim, time, vertices in input_data:
        if time not in time_instances:
            time_instances[time] = []
        time_instances[time].append((dim, vertices))

    # Create a 3D plot for each time instance
    for time, simplices in time_instances.items():
        fig = go.Figure()

        # Add vertices as scatter points (0-simplex)
        for v, pos in vertex_positions.items():
            fig.add_trace(go.Scatter3d(x=[pos[0]], y=[pos[1]], z=[pos[2]],
                                       mode='markers+text',
                                       text=[str(v)],
                                       textposition="top center",
                                       marker=dict(size=5, color='blue'),
                                       name=f'Vertex {v}'))

        # Add simplices (edges and triangles)
        for dim, vertices in simplices:
            if dim == 1:
                # Add 1-simplex (edge)
                v1, v2 = vertices
                fig.add_trace(go.Scatter3d(x=[vertex_positions[v1][0], vertex_positions[v2][0]],
                                           y=[vertex_positions[v1][1], vertex_positions[v2][1]],
                                           z=[vertex_positions[v1][2], vertex_positions[v2][2]],
                                           mode='lines', line=dict(color='red', width=3),
                                           name=f'Edge {v1}-{v2}'))
            elif dim == 2:
                # Add 2-simplex (triangle)
                v1, v2, v3 = vertices
                x = [vertex_positions[v1][0], vertex_positions[v2][0], vertex_positions[v3][0], vertex_positions[v1][0]]
                y = [vertex_positions[v1][1], vertex_positions[v2][1], vertex_positions[v3][1], vertex_positions[v1][1]]
                z = [vertex_positions[v1][2], vertex_positions[v2][2], vertex_positions[v3][2], vertex_positions[v1][2]]
                fig.add_trace(go.Mesh3d(x=x, y=y, z=z, color='green', opacity=0.5, name=f'Triangle {v1}-{v2}-{v3}'))

        # Set plot layout
        fig.update_layout(scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='cube'),
            title=f"Interactive 3D Simplices at Time {time}",
            showlegend=False
        )

        fig.show()

# Plot the simplices for each time instance
plot_simplices_3d_instances(input_data)
