import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from PIL import Image
import io
import base64
import time
import random

# Set page configuration
st.set_page_config(
    page_title="HYDROGEN HUB LOCATOR",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for retro gaming aesthetic
def load_css():
    css = """
    @import url('https://fonts.googleapis.com/css2?family=VT323&family=Space+Mono&display=swap');
    
    /* Main container */
    .main {
        background-color: #121212;
        color: #FFD700; /* Golden yellow for text */
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'VT323', monospace !important;
        color: #FF7F50 !important; /* Coral */
        text-shadow: 3px 3px 0px #000000;
        letter-spacing: 2px;
        margin-bottom: 20px !important;
    }
    
    /* Regular text */
    p, div, span, label {
        font-family: 'Space Mono', monospace !important;
        color: #FFD700 !important; /* Golden yellow */
    }
    
    /* Buttons */
    .stButton>button {
        font-family: 'VT323', monospace !important;
        background-color: #FF7F50 !important; /* Coral */
        color: #000000 !important;
        border: 3px solid #FFD700 !important; /* Golden yellow border */
        border-radius: 0px !important; /* Sharp edges */
        padding: 5px 20px !important;
        font-size: 20px !important;
        box-shadow: 5px 5px 0px #000000 !important;
        transition: all 0.1s !important;
    }
    
    .stButton>button:hover {
        transform: translate(2px, 2px) !important;
        box-shadow: 3px 3px 0px #000000 !important;
    }
    
    .stButton>button:active {
        transform: translate(5px, 5px) !important;
        box-shadow: 0px 0px 0px #000000 !important;
    }
    
    /* Sliders and number inputs */
    .stSlider>div>div, .stNumberInput>div>div {
        background-color: #FF7F50 !important; /* Coral */
    }
    
    /* Sidebar */
    .css-1d391kg, .css-12oz5g7 {
        background-color: #000000 !important;
        border-right: 3px solid #FF7F50 !important; /* Coral border */
    }
    
    /* Metric boxes */
    .css-1xarl3l, .css-1lsmgbg {
        background-color: #000000 !important;
        border: 3px solid #FF7F50 !important; /* Coral border */
        border-radius: 0px !important; /* Sharp edges */
        box-shadow: 5px 5px 0px #FFD700 !important; /* Golden yellow shadow */
        padding: 10px !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'VT323', monospace !important;
        background-color: #000000 !important;
        color: #FFD700 !important; /* Golden yellow */
        border: 2px solid #FF7F50 !important; /* Coral border */
        border-radius: 0px !important; /* Sharp edges */
        padding: 5px 20px !important;
        font-size: 18px !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FF7F50 !important; /* Coral */
        color: #000000 !important;
    }
    
    /* Tables */
    .stDataFrame {
        font-family: 'Space Mono', monospace !important;
        border: 3px solid #FF7F50 !important; /* Coral border */
    }
    
    .stDataFrame th {
        background-color: #FF7F50 !important; /* Coral */
        color: #000000 !important;
        font-family: 'VT323', monospace !important;
        font-size: 18px !important;
        padding: 8px !important;
    }
    
    .stDataFrame td {
        background-color: #000000 !important;
        color: #FFD700 !important; /* Golden yellow */
        font-family: 'Space Mono', monospace !important;
        border: 1px solid #FF7F50 !important; /* Coral border */
        padding: 8px !important;
    }
    
    /* Custom containers */
    .pixel-box {
        background-color: #000000;
        border: 3px solid #FF7F50; /* Coral border */
        padding: 20px;
        margin: 10px 0;
        box-shadow: 8px 8px 0px #FFD700; /* Golden yellow shadow */
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: #FF7F50 !important; /* Coral */
    }
    """
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Apply the custom CSS
load_css()

# Create a retro pixel art logo
def create_pixel_logo():
    # Create a simple pixel art hydrogen logo
    logo = [
        "                                ",
        "                                ",
        "             ██████             ",
        "         ████      ████         ",
        "       ██              ██       ",
        "     ██                  ██     ",
        "    ██                    ██    ",
        "   ██                      ██   ",
        "   ██                      ██   ",
        "   ██                      ██   ",
        "    ██                    ██    ",
        "     ██                  ██     ",
        "       ██              ██       ",
        "         ████      ████         ",
        "             ██████             ",
        "                                ",
        "                                ",
    ]
    
    # Define colors
    colors = {
        " ": (0, 0, 0, 0),  # Transparent
        "█": (255, 127, 80, 255),  # Coral color
    }
    
    # Create a pixel art image
    width = len(logo[0])
    height = len(logo)
    
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = img.load()
    
    for y in range(height):
        for x in range(width):
            if x < len(logo[y]):
                pixels[x, y] = colors[logo[y][x]]
    
    # Scale up the image
    scale = 10
    img = img.resize((width * scale, height * scale), Image.NEAREST)
    
    # Convert to base64 for display
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f'<img src="data:image/png;base64,{img_str}" width="200">'

# Create a blinking text effect
def blinking_text(text, size=24):
    return f"""
    <div style="font-family: 'VT323', monospace; font-size: {size}px; color: #FF7F50; text-align: center; animation: blink 1s infinite;">
        {text}
    </div>
    <style>
        @keyframes blink {{
            0% {{ opacity: 0; }}
            50% {{ opacity: 1; }}
            100% {{ opacity: 0; }}
        }}
    </style>
    """

# Function to simulate loading with retro game style
def loading_screen():
    st.markdown(blinking_text("LOADING SYSTEM...", 36), unsafe_allow_html=True)
    progress_text = st.empty()
    progress_bar = st.progress(0)
    
    for i in range(101):
        progress_text.markdown(f"<div style='font-family: VT323, monospace; color: #FFD700; font-size: 24px;'>SYSTEM BOOT: {i}%</div>", unsafe_allow_html=True)
        progress_bar.progress(i)
        time.sleep(0.01)
    
    progress_text.markdown(f"<div style='font-family: VT323, monospace; color: #FFD700; font-size: 24px;'>SYSTEM READY!</div>", unsafe_allow_html=True)
    time.sleep(0.5)
    progress_text.empty()
    progress_bar.empty()

# Generate sample data for demonstration
def generate_sample_sites(num_sites=50, region="FRANCE"):
    np.random.seed(42)  # For reproducibility
    
    if region.upper() == "FRANCE":
        # Rough bounds for France
        lat_min, lat_max = 42.0, 51.5
        lon_min, lon_max = -5.0, 9.0
    else:
        # Default bounds if region not recognized
        lat_min, lat_max = 40.0, 55.0
        lon_min, lon_max = -10.0, 10.0
    
    # Generate random locations
    latitudes = np.random.uniform(lat_min, lat_max, num_sites)
    longitudes = np.random.uniform(lon_min, lon_max, num_sites)
    
    # Generate random attributes for each site
    renewable_potential = np.random.uniform(50, 200, num_sites)  # MW
    grid_connection = np.random.uniform(0, 100, num_sites)  # % quality
    water_access = np.random.uniform(0, 100, num_sites)  # % availability
    land_cost = np.random.uniform(50, 500, num_sites)  # € per m²
    transport_access = np.random.uniform(0, 100, num_sites)  # % quality
    demand_proximity = np.random.uniform(0, 100, num_sites)  # % proximity
    environmental_impact = np.random.uniform(0, 100, num_sites)  # % impact (lower is better)
    
    # Site names (using major French cities and surrounding areas)
    french_locations = [
        "Paris-Nord", "Paris-Sud", "Marseille-Est", "Marseille-Ouest", 
        "Lyon-Nord", "Lyon-Sud", "Toulouse-Centre", "Toulouse-Ouest",
        "Nice-Côte", "Nantes-Loire", "Montpellier-Med", "Strasbourg-Rhin",
        "Bordeaux-Garonne", "Lille-Nord", "Rennes-Bretagne", "Reims-Champagne",
        "Le Havre-Maritime", "Saint-Étienne-Loire", "Toulon-Med", "Grenoble-Alpes",
        "Dijon-Bourgogne", "Angers-Loire", "Nîmes-Gard", "Villeurbanne-Rhône",
        "Le Mans-Sarthe", "Clermont-Ferrand", "Aix-Provence", "Brest-Finistère",
        "Tours-Loire", "Limoges-Limousin", "Amiens-Somme", "Annecy-Savoie",
        "Perpignan-Pyrénées", "Besançon-Doubs", "Metz-Lorraine", "Orléans-Loire",
        "Rouen-Normandie", "Mulhouse-Alsace", "Caen-Normandie", "Nancy-Lorraine",
        "Tourcoing-Nord", "Avignon-Vaucluse", "La Rochelle-Atlantique", "Troyes-Aube",
        "Dunkerque-Maritime", "Poitiers-Vienne", "Cherbourg-Manche", "Calais-Détroit",
        "Pau-Pyrénées", "Chalon-Saône"
    ]
    
    # Ensure we have enough names or cycle through them
    site_names = [french_locations[i % len(french_locations)] for i in range(num_sites)]
    
    # Create DataFrame
    data = {
        'site_name': site_names,
        'latitude': latitudes,
        'longitude': longitudes,
        'renewable_potential': renewable_potential,
        'grid_connection': grid_connection,
        'water_access': water_access,
        'land_cost': land_cost,
        'transport_access': transport_access,
        'demand_proximity': demand_proximity,
        'environmental_impact': environmental_impact
    }
    
    return pd.DataFrame(data)

# Calculate site scores based on weighted criteria
def calculate_site_scores(df, weights):
    # Create a copy of the DataFrame for scoring
    scored_df = df.copy()
    
    # Normalize each criterion to a 0-100 scale
    criteria = [
        'renewable_potential', 'grid_connection', 'water_access',
        'land_cost', 'transport_access', 'demand_proximity', 'environmental_impact'
    ]
    
    for criterion in criteria:
        if criterion in ['land_cost', 'environmental_impact']:
            # Lower values are better, so invert
            min_val = scored_df[criterion].min()
            max_val = scored_df[criterion].max()
            if max_val > min_val:
                scored_df[f'{criterion}_normalized'] = 100 * (1 - (scored_df[criterion] - min_val) / (max_val - min_val))
            else:
                scored_df[f'{criterion}_normalized'] = 100
        else:
            # Higher values are better
            min_val = scored_df[criterion].min()
            max_val = scored_df[criterion].max()
            if max_val > min_val:
                scored_df[f'{criterion}_normalized'] = 100 * (scored_df[criterion] - min_val) / (max_val - min_val)
            else:
                scored_df[f'{criterion}_normalized'] = 0
    
    # Calculate weighted score
    scored_df['total_score'] = 0
    
    for criterion in criteria:
        weight_key = f'{criterion}_weight'
        if weight_key in weights:
            scored_df['total_score'] += scored_df[f'{criterion}_normalized'] * weights[weight_key]
    
    # Round scores for display
    scored_df['total_score'] = scored_df['total_score'].round(2)
    
    # Rank sites
    scored_df['rank'] = scored_df['total_score'].rank(ascending=False, method='min').astype(int)
    
    return scored_df.sort_values('rank')

# Create a retro-style map using PyDeck
def create_retro_map(df, selected_site=None):
    # Make sure we're working with a copy
    map_df = df.copy()
    
    # Scale scores for visualization
    map_df['radius'] = 1000 + (map_df['total_score'] * 50)
    
    # Define color based on score
    def get_color(score):
        # Map score from 0-100 to color
        r = min(255, int(255 * (1 - score/100)))
        g = min(255, int(255 * (score/100)))
        b = 0
        return [r, g, b, 160]
    
    map_df['color'] = map_df['total_score'].apply(get_color)
    
    # Different styling for selected site
    if selected_site is not None:
        map_df.loc[map_df['site_name'] == selected_site, 'color'] = [255, 127, 80, 200]  # Coral
        map_df.loc[map_df['site_name'] == selected_site, 'radius'] = map_df.loc[map_df['site_name'] == selected_site, 'radius'] * 1.5
    
    # Create PyDeck map
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position=["longitude", "latitude"],
        get_radius="radius",
        get_fill_color="color",
        pickable=True,
        auto_highlight=True,
        opacity=0.8,
    )
    
    # Set initial view to center of France
    view_state = pdk.ViewState(
        latitude=46.603354,
        longitude=1.888334,
        zoom=5,
        pitch=0,
    )
    
    # Set map style to dark
    MAPBOX_STYLE = "mapbox://styles/mapbox/dark-v10"
    
    # Create tooltip
    tooltip = {
        "html": "<div style='font-family: VT323, monospace; color: #FFD700; background-color: #000000; border: 2px solid #FF7F50; padding: 10px;'>"
                "<b>Site:</b> {site_name}<br>"
                "<b>Score:</b> {total_score}<br>"
                "<b>Rank:</b> {rank}</div>",
        "style": {"backgroundColor": "#000000", "color": "#FFD700"}
    }
    
    # Create deck
    deck = pdk.Deck(
        map_style=MAPBOX_STYLE,
        initial_view_state=view_state,
        layers=[layer],
        tooltip=tooltip
    )
    
    return deck

# Generate a detailed site report
def generate_site_report(site_data, criteria_weights):
    # Extract data for the specific site
    site_name = site_data['site_name']
    total_score = site_data['total_score']
    rank = site_data['rank']
    
    # Create a radar chart for site attributes
    categories = [
        'Renewable\nPotential', 'Grid\nConnection', 'Water\nAccess',
        'Land\nCost', 'Transport\nAccess', 'Demand\nProximity', 'Environmental\nImpact'
    ]
    
    # Get normalized values
    values = [
        site_data['renewable_potential_normalized'],
        site_data['grid_connection_normalized'],
        site_data['water_access_normalized'],
        site_data['land_cost_normalized'],
        site_data['transport_access_normalized'],
        site_data['demand_proximity_normalized'],
        site_data['environmental_impact_normalized']
    ]
    
    # Create radar chart
    fig = go.Figure()
    
    # Add site data
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=site_name,
        line=dict(color='#FF7F50'),
        fillcolor='rgba(255, 127, 80, 0.5)'
    ))
    
    # Add average of top 5 sites for comparison if available
    if 'top_5_avg' in site_data:
        top_5_values = [
            site_data['top_5_avg']['renewable_potential_normalized'],
            site_data['top_5_avg']['grid_connection_normalized'],
            site_data['top_5_avg']['water_access_normalized'],
            site_data['top_5_avg']['land_cost_normalized'],
            site_data['top_5_avg']['transport_access_normalized'],
            site_data['top_5_avg']['demand_proximity_normalized'],
            site_data['top_5_avg']['environmental_impact_normalized']
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=top_5_values,
            theta=categories,
            fill='toself',
            name='Top 5 Avg',
            line=dict(color='#FFD700'),
            fillcolor='rgba(255, 215, 0, 0.3)'
        ))
    
    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color='#FFD700'),
                gridcolor='#333333'
            ),
            angularaxis=dict(
                tickfont=dict(color='#FFD700'),
                gridcolor='#333333'
            ),
            bgcolor='#000000'
        ),
        paper_bgcolor='#000000',
        plot_bgcolor='#000000',
        font=dict(
            family='VT323',
            size=16,
            color='#FFD700'
        ),
        legend=dict(
            font=dict(
                family='VT323',
                size=14,
                color='#FFD700'
            ),
            bgcolor='rgba(0, 0, 0, 0.7)',
            bordercolor='#FF7F50'
        ),
        margin=dict(l=40, r=40, t=30, b=30)
    )
    
    # Generate synthetic CAPEX/OPEX estimates
    electrolyzer_capacity = site_data['renewable_potential'] * 0.7  # MW
    capex = electrolyzer_capacity * 1.5  # Million €
    opex_yearly = capex * 0.04  # 4% of CAPEX per year
    
    # Estimate hydrogen production
    operating_hours = 4000 + (site_data['renewable_potential_normalized'] * 10)  # hours/year
    efficiency = 65 + (site_data['grid_connection_normalized'] * 0.1)  # %
    h2_production = electrolyzer_capacity * operating_hours * (efficiency/100) / 50  # tonnes/year (rough estimate)
    
    # Cost of hydrogen
    coh = (capex * 0.1 + opex_yearly) * 1000000 / (h2_production * 1000)  # €/kg
    
    # Return dictionary with all report info
    report = {
        'site_name': site_name,
        'total_score': total_score,
        'rank': rank,
        'radar_chart': fig,
        'capex': capex,
        'opex_yearly': opex_yearly,
        'electrolyzer_capacity': electrolyzer_capacity,
        'operating_hours': operating_hours,
        'efficiency': efficiency,
        'h2_production': h2_production,
        'cost_of_hydrogen': coh
    }
    
    return report

def create_capacity_factor_chart(renewable_potential, grid_quality):
    """Create a synthetic capacity factor chart based on site attributes"""
    # Generate synthetic monthly capacity factors
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Base capacity factors for solar and wind with seasonal variations
    base_solar = np.array([0.15, 0.18, 0.22, 0.25, 0.28, 0.30, 0.32, 0.30, 0.25, 0.20, 0.16, 0.14])
    base_wind = np.array([0.35, 0.32, 0.30, 0.25, 0.20, 0.18, 0.15, 0.18, 0.22, 0.28, 0.32, 0.35])
    
    # Scale based on renewable potential (0-100 normalized)
    potential_factor = renewable_potential / 100.0
    grid_factor = grid_quality / 100.0
    
    # Apply scaling and add some random variation
    np.random.seed(42)  # For reproducibility
    solar_cf = base_solar * potential_factor * (0.8 + 0.4 * np.random.random(12))
    wind_cf = base_wind * potential_factor * (0.8 + 0.4 * np.random.random(12))
    
    # Calculate combined capacity factor (assuming 70% wind, 30% solar)
    combined_cf = 0.7 * wind_cf + 0.3 * solar_cf
    
    # Calculate grid availability based on grid connection quality
    grid_availability = 0.95 + (grid_factor * 0.05)
    
    # Create figure
    fig = go.Figure()
    
    # Add traces
    fig.add_trace(go.Scatter(
        x=months,
        y=wind_cf,
        mode='lines+markers',
        name='Wind CF',
        line=dict(color='#00FFFF', width=2),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=months,
        y=solar_cf,
        mode='lines+markers',
        name='Solar CF',
        line=dict(color='#FFFF00', width=2),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=months,
        y=combined_cf,
        mode='lines+markers',
        name='Combined CF',
        line=dict(color='#FF7F50', width=3),
        marker=dict(size=10)
    ))
    
    # Add a line for grid availability
    fig.add_trace(go.Scatter(
        x=months,
        y=[grid_availability] * 12,
        mode='lines',
        name='Grid Availability',
        line=dict(color='#FFD700', width=2, dash='dash')
    ))
    
    # Update layout
    fig.update_layout(
        title='Monthly Capacity Factors',
        xaxis_title='Month',
        yaxis_title='Capacity Factor',
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font=dict(
            family='VT323',
            size=16,
            color='#FFD700'
        ),
        legend=dict(
            font=dict(
                family='VT323',
                size=14,
                color='#FFD700'
            ),
            bgcolor='rgba(0, 0, 0, 0.7)',
            bordercolor='#FF7F50'
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='#333333',
            gridwidth=1,
            showline=True,
            linecolor='#FF7F50',
            linewidth=2,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#333333',
            gridwidth=1,
            showline=True,
            linecolor='#FF7F50',
            linewidth=2,
            range=[0, 0.5]
        ),
        margin=dict(l=10, r=10, t=50, b=10),
    )
    
    return fig

# Main function
def main():
    # Logo and title
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(create_pixel_logo(), unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; font-size: 48px; margin-top: 0;'>HYDROGEN HUB LOCATOR</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; margin-top: 0;'>MULTI-CRITERIA GEOSPATIAL EDITION</h3>", unsafe_allow_html=True)
    
    # Simulated loading screen at startup
    if 'loaded' not in st.session_state:
        loading_screen()
        st.session_state.loaded = True
    
    # Initialize session state variables
    if 'sites_data' not in st.session_state:
        st.session_state.sites_data = generate_sample_sites(num_sites=50, region="FRANCE")
    
    if 'criteria_weights' not in st.session_state:
        st.session_state.criteria_weights = {
            'renewable_potential_weight': 0.20,
            'grid_connection_weight': 0.15,
            'water_access_weight': 0.10,
            'land_cost_weight': 0.15,
            'transport_access_weight': 0.10,
            'demand_proximity_weight': 0.20,
            'environmental_impact_weight': 0.10
        }
    
    if 'scored_sites' not in st.session_state or st.session_state.update_scores:
        st.session_state.scored_sites = calculate_site_scores(
            st.session_state.sites_data, 
            st.session_state.criteria_weights
        )
        if 'update_scores' in st.session_state:
            st.session_state.update_scores = False
    
    # Sidebar navigation
    st.sidebar.markdown("<h2 style='text-align: center;'>CONTROL PANEL</h2>", unsafe_allow_html=True)
    
    # Data options
    st.sidebar.markdown("<div class='pixel-box'><h3 style='margin-top: 0;'>DATA SOURCE</h3></div>", unsafe_allow_html=True)
    data_source = st.sidebar.radio(
        "Select data source:",
        ["Upload CSV", "Use Sample Data"],
        key="data_source"
    )
    
    region_options = ["FRANCE", "SPAIN", "GERMANY", "ITALY"]
    region = st.sidebar.selectbox("Target Region:", region_options, index=0)
    
    if data_source == "Upload CSV":
        uploaded_file = st.sidebar.file_uploader("Upload your CSV file:", type="csv")
        if uploaded_file is not None:
            st.session_state.sites_data = pd.read_csv(uploaded_file)
            st.session_state.update_scores = True
        else:
            st.sidebar.markdown(blinking_text("NO DATA LOADED"), unsafe_allow_html=True)
    else:
        st.sidebar.markdown("<div style='text-align: center;'>🎲 RANDOM SITE GENERATOR 🎲</div>", unsafe_allow_html=True)
        num_sites = st.sidebar.slider("Number of sites:", min_value=10, max_value=100, value=50, step=5)
        
        if st.sidebar.button("GENERATE NEW SITES"):
            st.session_state.sites_data = generate_sample_sites(num_sites=num_sites, region=region)
            st.session_state.update_scores = True
            st.sidebar.success("NEW SITES GENERATED!")
    
    # Criteria weights
    st.sidebar.markdown("<div class='pixel-box'><h3 style='margin-top: 0;'>CRITERIA WEIGHTS</h3></div>", unsafe_allow_html=True)
    st.sidebar.markdown("<div style='font-size: 14px;'>Adjust importance of each factor (total = 100%)</div>", unsafe_allow_html=True)
    
    # Input weights with sliders
    renewable_weight = st.sidebar.slider(
        "Renewable Potential:", 
        min_value=0.0, 
        max_value=1.0, 
        value=st.session_state.criteria_weights.get('renewable_potential_weight', 0.2),
        step=0.05,
        format="%.2f"
    )
    
    grid_weight = st.sidebar.slider(
        "Grid Connection:", 
        min_value=0.0, 
        max_value=1.0, 
        value=st.session_state.criteria_weights.get('grid_connection_weight', 0.15),
        step=0.05,
        format="%.2f"
    )
    
    water_weight = st.sidebar.slider(
        "Water Access:", 
        min_value=0.0, 
        max_value=1.0, 
        value=st.session_state.criteria_weights.get('water_access_weight', 0.1),
        step=0.05,
        format="%.2f"
    )
    
    land_weight = st.sidebar.slider(
        "Land Cost:", 
        min_value=0.0, 
        max_value=1.0, 
        value=st.session_state.criteria_weights.get('land_cost_weight', 0.15),
        step=0.05,
        format="%.2f"
    )
    
    transport_weight = st.sidebar.slider(
        "Transport Access:", 
        min_value=0.0, 
        max_value=1.0, 
        value=st.session_state.criteria_weights.get('transport_access_weight', 0.1),
        step=0.05,
        format="%.2f"
    )
    
    demand_weight = st.sidebar.slider(
        "Demand Proximity:", 
        min_value=0.0, 
        max_value=1.0, 
        value=st.session_state.criteria_weights.get('demand_proximity_weight', 0.2),
        step=0.05,
        format="%.2f"
    )
    
    env_weight = st.sidebar.slider(
        "Environmental Impact:", 
        min_value=0.0, 
        max_value=1.0, 
        value=st.session_state.criteria_weights.get('environmental_impact_weight', 0.1),
        step=0.05,
        format="%.2f"
    )
    
    # Calculate total and normalize if needed
    total_weight = renewable_weight + grid_weight + water_weight + land_weight + transport_weight + demand_weight + env_weight
    
    if abs(total_weight - 1.0) > 0.001:  # If not very close to 1.0
        st.sidebar.warning(f"Total weight: {total_weight:.2f} ≠ 1.0! Weights will be normalized.")
        
        # Update weights normalized to sum to 1.0
        renewable_weight /= total_weight
        grid_weight /= total_weight
        water_weight /= total_weight
        land_weight /= total_weight
        transport_weight /= total_weight
        demand_weight /= total_weight
        env_weight /= total_weight
    
    # Store weights in session state
    new_weights = {
        'renewable_potential_weight': renewable_weight,
        'grid_connection_weight': grid_weight,
        'water_access_weight': water_weight,
        'land_cost_weight': land_weight,
        'transport_access_weight': transport_weight,
        'demand_proximity_weight': demand_weight,
        'environmental_impact_weight': env_weight
    }
    
    # Check if weights have changed
    if new_weights != st.session_state.criteria_weights:
        st.session_state.criteria_weights = new_weights
        st.session_state.update_scores = True
    
    # Run analysis button
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    run_analysis = st.sidebar.button("► RUN ANALYSIS ◄", key="run_analysis")
    
    # Credits
    st.sidebar.markdown("<br><br><div style='text-align: center; font-size: 12px; opacity: 0.7;'>© 2025 HYDROGEN HUB LOCATOR</div>", unsafe_allow_html=True)
    
    # Run analysis if requested
    if run_analysis or 'update_scores' in st.session_state and st.session_state.update_scores:
        st.session_state.scored_sites = calculate_site_scores(
            st.session_state.sites_data, 
            st.session_state.criteria_weights
        )
        st.session_state.update_scores = False
    
    # Main content area with tabs
    tabs = st.tabs(["MAP VIEW", "SITE RANKING", "DETAILED ANALYSIS", "DATA EXPLORER"])
    
    with tabs[0]:  # MAP VIEW
        st.markdown("<h2>MAP VIEW</h2>", unsafe_allow_html=True)
        
        # Display top sites metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<div class='pixel-box'>", unsafe_allow_html=True)
            top_site = st.session_state.scored_sites.iloc[0]
            st.metric(
                "TOP SITE",
                top_site['site_name'],
                f"Score: {top_site['total_score']:.1f}"
            )
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='pixel-box'>", unsafe_allow_html=True)
            avg_score = st.session_state.scored_sites['total_score'].mean()
            top5_avg = st.session_state.scored_sites.head(5)['total_score'].mean()
            st.metric(
                "AVERAGE SCORE",
                f"{avg_score:.1f}",
                f"{top5_avg - avg_score:.1f} (Top 5)"
            )
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown("<div class='pixel-box'>", unsafe_allow_html=True)
            site_count = len(st.session_state.scored_sites)
            viable_sites = len(st.session_state.scored_sites[st.session_state.scored_sites['total_score'] > 70])
            st.metric(
                "TOTAL SITES",
                f"{site_count}",
                f"{viable_sites} Viable"
            )
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Map container
        st.markdown("<div class='pixel-box'>", unsafe_allow_html=True)
        st.markdown("<h3>SITE LOCATION MAP</h3>", unsafe_allow_html=True)
        
        # Selected site for highlighting
        site_options = ["None"] + st.session_state.scored_sites['site_name'].tolist()
        selected_site = st.selectbox("Highlight Site:", site_options)
        
        if selected_site == "None":
            selected_site = None
        
        # Create and display map
        map_deck = create_retro_map(st.session_state.scored_sites, selected_site)
        st.pydeck_chart(map_deck)
        
        st.markdown("<div style='font-size: 14px; text-align: center;'>Sites colored by score (green = higher score). Click on sites for details.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Legend box
        st.markdown("<div class='pixel-box'>", unsafe_allow_html=True)
        st.markdown("<h3>SCORING LEGEND</h3>", unsafe_allow_html=True)
        
        # Display the weights used for scoring
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div style='font-family: VT323, monospace; font-size: 18px;'>", unsafe_allow_html=True)
            st.markdown(f"🌞 Renewable Potential: {st.session_state.criteria_weights['renewable_potential_weight']:.2f}", unsafe_allow_html=True)
            st.markdown(f"⚡ Grid Connection: {st.session_state.criteria_weights['grid_connection_weight']:.2f}", unsafe_allow_html=True)
            st.markdown(f"💧 Water Access: {st.session_state.criteria_weights['water_access_weight']:.2f}", unsafe_allow_html=True)
            st.markdown(f"🏞️ Land Cost: {st.session_state.criteria_weights['land_cost_weight']:.2f}", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div style='font-family: VT323, monospace; font-size: 18px;'>", unsafe_allow_html=True)
            st.markdown(f"🚚 Transport Access: {st.session_state.criteria_weights['transport_access_weight']:.2f}", unsafe_allow_html=True)
            st.markdown(f"🏭 Demand Proximity: {st.session_state.criteria_weights['demand_proximity_weight']:.2f}", unsafe_allow_html=True)
            st.markdown(f"🌱 Environmental Impact: {st.session_state.criteria_weights['environmental_impact_weight']:.2f}", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[1]:  # SITE RANKING
        st.markdown("<h2>SITE RANKING</h2>", unsafe_allow_html=True)
        
        # Top sites summary
        st.markdown("<div class='pixel-box'>", unsafe_allow_html=True)
        st.markdown("<h3>TOP 10 HYDROGEN HUB LOCATIONS</h3>", unsafe_allow_html=True)
        
        # Display bar chart of top sites
        top_sites = st.session_state.scored_sites.head(10).copy()
        
        fig = px.bar(
            top_sites,
            x='site_name',
            y='total_score',
            color='total_score',
            color_continuous_scale=["#FF0000", "#FFFF00", "#00FF00"],
            labels={'site_name': 'Site Location', 'total_score': 'Score'},
            title="Top 10 Sites by Overall Score"
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            plot_bgcolor='#000000',
            paper_bgcolor='#000000',
            font=dict(
                family='VT323',
                size=16,
                color='#FFD700'
            ),
            coloraxis_colorbar=dict(
                title="Score",
                titlefont=dict(color='#FFD700'),
                tickfont=dict(color='#FFD700')
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor='#333333',
                gridwidth=1,
                showline=True,
                linecolor='#FF7F50',
                linewidth=2,
                title_font=dict(color='#FFD700')
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#333333',
                gridwidth=1,
                showline=True,
                linecolor='#FF7F50',
                linewidth=2,
                title_font=dict(color='#FFD700')
            ),
            margin=dict(l=10, r=10, t=50, b=10),
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Criteria breakdown
        st.markdown("<div class='pixel-box'>", unsafe_allow_html=True)
        st.markdown("<h3>CRITERIA BREAKDOWN</h3>", unsafe_allow_html=True)
        
        # Get the top 5 sites
        top5_sites = st.session_state.scored_sites.head(5).copy()
        
        # Prepare data for heatmap
        criteria_cols = [
            'renewable_potential_normalized', 'grid_connection_normalized', 
            'water_access_normalized', 'land_cost_normalized',
            'transport_access_normalized', 'demand_proximity_normalized', 
            'environmental_impact_normalized'
        ]
        
        criteria_labels = [
            'Renewable\nPotential', 'Grid\nConnection', 'Water\nAccess',
            'Land\nCost', 'Transport\nAccess', 'Demand\nProximity', 'Environmental\nImpact'
        ]
        
        heatmap_data = top5_sites[criteria_cols].copy()
        heatmap_data.columns = criteria_labels
        heatmap_data.index = top5_sites['site_name']
        
        # Create heatmap
        fig = px.imshow(
            heatmap_data,
            color_continuous_scale=["#FF0000", "#FFFF00", "#00FF00"],
            labels=dict(x="Criteria", y="Site", color="Score"),
            text_auto=True
        )
        
        fig.update_layout(
            title="Top 5 Sites Criteria Scores",
            plot_bgcolor='#000000',
            paper_bgcolor='#000000',
            font=dict(
                family='VT323',
                size=16,
                color='#FFD700'
            ),
            coloraxis_colorbar=dict(
                title="Score",
                titlefont=dict(color='#FFD700'),
                tickfont=dict(color='#FFD700')
            ),
            margin=dict(l=10, r=10, t=50, b=30),
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Complete ranking table
        st.markdown("<div class='pixel-box'>", unsafe_allow_html=True)
        st.markdown("<h3>COMPLETE SITE RANKING</h3>", unsafe_allow_html=True)
        
        # Prepare a clean display version of the dataframe
        display_df = st.session_state.scored_sites.copy()
        
        # Select and rename columns for display
        display_cols = [
            'rank', 'site_name', 'total_score', 
            'renewable_potential', 'grid_connection', 'water_access',
            'land_cost', 'transport_access', 'demand_proximity', 'environmental_impact'
        ]
        
        display_df = display_df[display_cols].round(2)
        
        # Display the dataframe
        st.dataframe(display_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[2]:  # DETAILED ANALYSIS
        st.markdown("<h2>DETAILED ANALYSIS</h2>", unsafe_allow_html=True)
        
        # Site selector
        selected_site_for_analysis = st.selectbox(
            "Select Site for Detailed Analysis:",
            st.session_state.scored_sites['site_name'].tolist(),
            index=0
        )
        
        if selected_site_for_analysis:
            # Get site data
            site_data = st.session_state.scored_sites[st.session_state.scored_sites['site_name'] == selected_site_for_analysis].iloc[0].to_dict()
            
            # Add avg of top 5 sites for comparison
            top5_avg = st.session_state.scored_sites.head(5)[criteria_cols].mean().to_dict()
            site_data['top_5_avg'] = top5_avg
            
            # Generate site report
            site_report = generate_site_report(site_data, st.session_state.criteria_weights)
            
            # Site overview
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("<div class='pixel-box' style='text-align: center;'>", unsafe_allow_html=True)
                st.markdown(f"<h3>{site_report['site_name']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size: 24px; margin-bottom: 10px;'>RANK: #{site_report['rank']} | SCORE: {site_report['total_score']:.1f}</div>", unsafe_allow_html=True)
                
                # Display lat/long
                lat = site_data['latitude']
                lon = site_data['longitude']
                st.markdown(f"<div style='font-size: 18px;'>Location: {lat:.4f}°N, {lon:.4f}°E</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Site criteria radar chart
            st.markdown("<div class='pixel-box'>", unsafe_allow_html=True)
            st.markdown("<h3>SITE CRITERIA ANALYSIS</h3>", unsafe_allow_html=True)
            
            st.plotly_chart(site_report['radar_chart'], use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Site economics
            st.markdown("<div class='pixel-box'>", unsafe_allow_html=True)
            st.markdown("<h3>HYDROGEN PRODUCTION ECONOMICS</h3>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "ELECTROLYZER CAPACITY",
                    f"{site_report['electrolyzer_capacity']:.1f} MW"
                )
            
            with col2:
                st.metric(
                    "CAPEX",
                    f"€{site_report['capex']:.1f}M"
                )
            
            with col3:
                st.metric(
                    "ANNUAL OPEX",
                    f"€{site_report['opex_yearly']:.2f}M"
                )
            
            with col4:
                st.metric(
                    "H₂ PRODUCTION",
                    f"{site_report['h2_production']:.0f} t/year"
                )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "OPERATING HOURS",
                    f"{site_report['operating_hours']:.0f} h/year"
                )
            
            with col2:
                st.metric(
                    "EFFICIENCY",
                    f"{site_report['efficiency']:.1f}%"
                )
            
            with col3:
                st.metric(
                    "COST OF HYDROGEN",
                    f"€{site_report['cost_of_hydrogen']:.2f}/kg"
                )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Capacity factor chart
            st.markdown("<div class='pixel-box'>", unsafe_allow_html=True)
            st.markdown("<h3>RENEWABLE CAPACITY FACTORS</h3>", unsafe_allow_html=True)
            
            # Create capacity factor chart based on site attributes
            cf_chart = create_capacity_factor_chart(
                site_data['renewable_potential_normalized'],
                site_data['grid_connection_normalized']
            )
            
            st.plotly_chart(cf_chart, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # SWOT Analysis
            st.markdown("<div class='pixel-box'>", unsafe_allow_html=True)
            st.markdown("<h3>SWOT ANALYSIS</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div style='background-color: rgba(0, 255, 0, 0.1); border: 2px solid #00FF00; padding: 10px;'>", unsafe_allow_html=True)
                st.markdown("<h4 style='color: #00FF00;'>STRENGTHS</h4>", unsafe_allow_html=True)
                
                # Identify strengths (top 3 criteria)
                criteria_values = {
                    'Renewable Potential': site_data['renewable_potential_normalized'],
                    'Grid Connection': site_data['grid_connection_normalized'],
                    'Water Access': site_data['water_access_normalized'],
                    'Land Cost': site_data['land_cost_normalized'],
                    'Transport Access': site_data['transport_access_normalized'],
                    'Demand Proximity': site_data['demand_proximity_normalized'],
                    'Environmental Impact': site_data['environmental_impact_normalized']
                }
                
                strengths = sorted(criteria_values.items(), key=lambda x: x[1], reverse=True)[:3]
                
                for strength, value in strengths:
                    st.markdown(f"• <b>{strength}:</b> {value:.1f}/100", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div style='background-color: rgba(255, 0, 0, 0.1); border: 2px solid #FF0000; padding: 10px;'>", unsafe_allow_html=True)
                st.markdown("<h4 style='color: #FF0000;'>WEAKNESSES</h4>", unsafe_allow_html=True)
                
                # Identify weaknesses (bottom 3 criteria)
                weaknesses = sorted(criteria_values.items(), key=lambda x: x[1])[:3]
                
                for weakness, value in weaknesses:
                    st.markdown(f"• <b>{weakness}:</b> {value:.1f}/100", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div style='background-color: rgba(255, 215, 0, 0.1); border: 2px solid #FFD700; padding: 10px; margin-top: 10px;'>", unsafe_allow_html=True)
                st.markdown("<h4 style='color: #FFD700;'>OPPORTUNITIES</h4>", unsafe_allow_html=True)
                
                # Generate synthetic opportunities based on site attributes
                opportunities = []
                
                if site_data['renewable_potential_normalized'] > 70:
                    opportunities.append("Potential for renewable energy expansion")
                
                if site_data['grid_connection_normalized'] > 60:
                    opportunities.append("Strong grid connection for power reliability")
                
                if site_data['demand_proximity_normalized'] > 70:
                    opportunities.append("Close proximity to hydrogen consumers")
                
                if site_data['transport_access_normalized'] > 65:
                    opportunities.append("Good logistics infrastructure for distribution")
                
                if len(opportunities) < 3:
                    opportunities.append("Regional hydrogen hub development incentives")
                    opportunities.append("Integration with existing energy systems")
                
                for opportunity in opportunities[:3]:
                    st.markdown(f"• {opportunity}", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div style='background-color: rgba(0, 191, 255, 0.1); border: 2px solid #00BFFF; padding: 10px; margin-top: 10px;'>", unsafe_allow_html=True)
                st.markdown("<h4 style='color: #00BFFF;'>THREATS</h4>", unsafe_allow_html=True)
                
                # Generate synthetic threats based on site attributes
                threats = []
                
                if site_data['environmental_impact_normalized'] < 50:
                    threats.append("Potential environmental permitting challenges")
                
                if site_data['water_access_normalized'] < 60:
                    threats.append("Water access constraints during dry periods")
                
                if site_data['land_cost_normalized'] < 50:
                    threats.append("Rising land acquisition costs")
                
                if len(threats) < 3:
                    threats.append("Evolving hydrogen market regulations")
                    threats.append("Competition from other emerging energy hubs")
                    threats.append("Technology cost fluctuations")
                
                for threat in threats[:3]:
                    st.markdown(f"• {threat}", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Recommendations
            st.markdown("<div class='pixel-box'>", unsafe_allow_html=True)
            st.markdown("<h3>RECOMMENDATIONS</h3>", unsafe_allow_html=True)
            
            # Generate synthetic recommendations based on site analysis
            recommendations = [
                f"<b>Initial Capacity:</b> Deploy {site_report['electrolyzer_capacity']:.1f} MW electrolyzer capacity in phase 1",
                f"<b>Technology:</b> {'PEM electrolyzer technology' if site_data['grid_connection_normalized'] > 70 else 'Alkaline electrolyzer technology'} most suitable for this location",
                f"<b>Renewable Mix:</b> {'Wind-dominated' if site_data['latitude'] > 48 else 'Solar-dominated' if site_data['latitude'] < 44 else 'Balanced wind/solar'} renewable energy mix recommended",
                f"<b>Grid Strategy:</b> {'Strong emphasis on grid connection for reliability' if site_data['grid_connection_normalized'] > 65 else 'Focus on expanding local renewable capacity to reduce grid dependency'}",
                f"<b>Water Management:</b> {'Standard water supply infrastructure sufficient' if site_data['water_access_normalized'] > 70 else 'Investment in water treatment and recycling systems recommended'}",
                f"<b>Next Steps:</b> Conduct detailed site survey and initiate permitting process"
            ]
            
            for recommendation in recommendations:
                st.markdown(f"• {recommendation}", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        else:
            st.markdown("<div class='pixel-box' style='text-align: center;'>", unsafe_allow_html=True)
            st.markdown(blinking_text("SELECT A SITE FOR DETAILED ANALYSIS", 28), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[3]:  # DATA EXPLORER
        st.markdown("<h2>DATA EXPLORER</h2>", unsafe_allow_html=True)
        
        # Raw data table
        st.markdown("<div class='pixel-box'>", unsafe_allow_html=True)
        st.markdown("<h3>RAW DATA</h3>", unsafe_allow_html=True)
        
        # Display the data
        st.dataframe(st.session_state.sites_data, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Data statistics
        st.markdown("<div class='pixel-box'>", unsafe_allow_html=True)
        st.markdown("<h3>DATA STATISTICS</h3>", unsafe_allow_html=True)
        
        # Calculate statistics
        numeric_cols = st.session_state.sites_data.select_dtypes(include=['number']).columns
        stats_df = st.session_state.sites_data[numeric_cols].describe().round(2)
        
        st.dataframe(stats_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Correlation matrix
        st.markdown("<div class='pixel-box'>", unsafe_allow_html=True)
        st.markdown("<h3>CORRELATION MATRIX</h3>", unsafe_allow_html=True)
        
        # Calculate correlation matrix
        criterion_cols = [
            'renewable_potential', 'grid_connection', 'water_access',
            'land_cost', 'transport_access', 'demand_proximity', 'environmental_impact'
        ]
        
        corr_matrix = st.session_state.sites_data[criterion_cols].corr().round(2)
        
        # Create correlation heatmap
        fig = px.imshow(
            corr_matrix,
            color_continuous_scale=["#000000", "#3366CC", "#FFD700", "#FF7F50"],
            labels=dict(x="Criteria", y="Criteria", color="Correlation"),
            text_auto=True
        )
        
        fig.update_layout(
            title='Criteria Correlation Matrix',
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(
                family="VT323",
                size=16,
                color="#FFD700"
            ),
            coloraxis_colorbar=dict(
                title="Correlation",
                thicknessmode="pixels",
                thickness=20,
                tickfont=dict(
                    family="VT323",
                    size=14,
                    color="#FFD700"
                )
            ),
            margin=dict(l=10, r=10, t=50, b=10),
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Criteria distributions
        st.markdown("<div class='pixel-box'>", unsafe_allow_html=True)
        st.markdown("<h3>CRITERIA DISTRIBUTIONS</h3>", unsafe_allow_html=True)
        
        # Create distribution plots
        selected_criterion = st.selectbox(
            "Select criterion to visualize:",
            criterion_cols
        )
        
        fig = px.histogram(
            st.session_state.sites_data,
            x=selected_criterion,
            nbins=20,
            color_discrete_sequence=["#FF7F50"],
            title=f"Distribution of {selected_criterion}"
        )
        
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(
                family="VT323",
                size=16,
                color="#FFD700"
            ),
            xaxis=dict(
                title=selected_criterion,
                showgrid=True,
                gridcolor='#333333',
                gridwidth=1,
                showline=True,
                linecolor='#FF7F50',
                linewidth=2,
                title_font=dict(color='#FFD700')
            ),
            yaxis=dict(
                title="Count",
                showgrid=True,
                gridcolor='#333333',
                gridwidth=1,
                showline=True,
                linecolor='#FF7F50',
                linewidth=2,
                title_font=dict(color='#FFD700')
            ),
            margin=dict(l=10, r=10, t=50, b=10),
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add scatter plot of two criteria
        st.markdown("<h4>CRITERIA RELATIONSHIPS</h4>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            x_axis = st.selectbox("X-Axis:", criterion_cols, index=0)
        
        with col2:
            y_axis = st.selectbox("Y-Axis:", criterion_cols, index=1)
        
        fig = px.scatter(
            st.session_state.sites_data,
            x=x_axis,
            y=y_axis,
            color='site_name',
            title=f"{x_axis} vs {y_axis}",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(
                family="VT323",
                size=16,
                color="#FFD700"
            ),
            xaxis=dict(
                title=x_axis,
                showgrid=True,
                gridcolor='#333333',
                gridwidth=1,
                showline=True,
                linecolor='#FF7F50',
                linewidth=2,
                title_font=dict(color='#FFD700')
            ),
            yaxis=dict(
                title=y_axis,
                showgrid=True,
                gridcolor='#333333',
                gridwidth=1,
                showline=True,
                linecolor='#FF7F50',
                linewidth=2,
                title_font=dict(color='#FFD700')
            ),
            margin=dict(l=10, r=10, t=50, b=10),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    main()