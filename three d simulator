import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Page Config
st.set_page_config(
    page_title="NCERT 3D Science & Math Simulators",
    page_icon="🔬",
    layout="wide"
)

# Sidebar Navigation
st.sidebar.title("📚 NCERT 3D Simulators")
subject = st.sidebar.selectbox("Select Subject", ["Physics", "Chemistry", "Mathematics"])

if subject == "Chemistry":
    chapter = st.sidebar.selectbox("Select Chapter", [
        "Class 9: Bohr's Atomic Model", 
        "Class 12: Crystal Lattice (Unit Cell)"
    ])
elif subject == "Physics":
    chapter = st.sidebar.selectbox("Select Chapter", [
        "Class 11: 3D Vector Addition", 
        "Class 11: Projectile Motion Trajectory"
    ])
else:
    chapter = st.sidebar.selectbox("Select Chapter", [
        "Class 11/12: 3D Coordinate Geometry & Planes", 
        "Class 12: 3D Line Intersection"
    ])

st.title(f"🚀 {chapter}")
st.markdown("---")

# --- 1. CHEMISTRY: CLASS 9 BOHR'S ATOMIC MODEL ---
if chapter == "Class 9: Bohr's Atomic Model":
    st.subheader("Interactive 3D Bohr Model of an Atom")
    st.write("Visualize the nucleus surrounded by revolving electron orbits in three dimensions.")
    
    num_orbits = st.slider("Select Number of Shells (Orbits)", 1, 3, 2)
    
    # Create 3D plot
    fig = go.Figure()
    
    # Nucleus
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers',
        marker=dict(size=15, color='red'),
        name='Nucleus (Protons + Neutrons)'
    ))
    
    # Generate Orbits and Electrons
    t = np.linspace(0, 2 * np.pi, 100)
    for i in range(1, num_orbits + 1):
        radius = i * 2.0
        # Orbit ring (XY plane)
        fig.add_trace(go.Scatter3d(
            x=radius * np.cos(t), y=radius * np.sin(t), z=np.zeros_like(t),
            mode='lines', line=dict(color='gray', width=2),
            name=f'Shell {i} Path'
        ))
        # Electron position
        fig.add_trace(go.Scatter3d(
            x=[radius * np.cos(i)], y=[radius * np.sin(i)], z=[0],
            mode='markers', marker=dict(size=8, color='cyan'),
            name=f'Electron in Shell {i}'
        ))

    fig.update_layout(
        scene=dict(xaxis_title='X Axis', yaxis_title='Y Axis', zaxis_title='Z Axis'),
        margin=dict(l=0, r=0, b=0, t=0),
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 2. PHYSICS: CLASS 11 3D VECTOR ADDITION ---
elif chapter == "Class 11: 3D Vector Addition":
    st.subheader("Vector Addition in 3D Space ($\vec{R} = \vec{A} + \vec{B}$)")
    
    col1, col2 = st.columns(2)
    with col1:
        ax = st.slider("Vector A (X)", -5.0, 5.0, 3.0)
        ay = st.slider("Vector A (Y)", -5.0, 5.0, 1.0)
        az = st.slider("Vector A (Z)", -5.0, 5.0, 2.0)
    with col2:
        bx = st.slider("Vector B (X)", -5.0, 5.0, 1.0)
        by = st.slider("Vector B (Y)", -5.0, 5.0, 4.0)
        bz = st.slider("Vector B (Z)", -5.0, 5.0, -2.0)
        
    rx, ry, rz = ax + bx, ay + by, az + bz
    
    fig = go.Figure()
    # Vector A
    fig.add_trace(go.Cone(x=[0], y=[0], z=[0], u=[ax], v=[ay], w=[az], 
                          colorscale='Blues', name='Vector A', showscale=False))
    # Vector B (starting from tip of A)
    fig.add_trace(go.Cone(x=[ax], y=[ay], z=[az], u=[bx], v=[by], w=[bz], 
                          colorscale='Greens', name='Vector B', showscale=False))
    # Resultant Vector R
    fig.add_trace(go.Cone(x=[0], y=[0], z=[0], u=[rx], v=[ry], w=[rz], 
                          colorscale='Reds', name='Resultant R', showscale=False))

    fig.update_layout(
        scene=dict(xaxis=dict(range=[-10, 10]), yaxis=dict(range=[-10, 10]), zaxis=dict(range=[-10, 10])),
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.success(f"Resultant Vector Coordinates: R = ({rx:.1f}, {ry:.1f}, {rz:.1f})")

# --- 3. MATHEMATICS: 3D COORDINATE GEOMETRY ---
elif chapter == "Class 11/12: 3D Coordinate Geometry & Planes":
    st.subheader("Plotting Points and Planes in 3D Space")
    
    px = st.number_input("Point X coordinate", value=3.0)
    py = st.number_input("Point Y coordinate", value=4.0)
    pz = st.number_input("Point Z coordinate", value=5.0)

    fig = go.Figure()
    
    # Point P
    fig.add_trace(go.Scatter3d(
        x=[px], y=[py], z=[pz],
        mode='text+markers',
        text=[f"P({px},{py},{pz})"],
        marker=dict(size=8, color='magenta')
    ))
    
    # Coordinate Axes lines
    fig.add_trace(go.Scatter3d(x=[-5, 5], y=[0, 0], z=[0, 0], mode='lines', line=dict(color='red', width=4), name='X-Axis'))
    fig.add_trace(go.Scatter3d(x=[0, 0], y=[-5, 5], z=[0, 0], mode='lines', line=dict(color='green', width=4), name='Y-Axis'))
    fig.add_trace(go.Scatter3d(x=[0, 0], y=[0, 0], z=[-5, 5], mode='lines', line=dict(color='blue', width=4), name='Z-Axis'))

    fig.update_layout(
        scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Select a chapter from the sidebar to load the 3D interactive model.")
