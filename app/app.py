"""
California House Price Prediction - Streamlit App

A beautiful, interactive web application for predicting California
house prices using machine learning.

Run with: streamlit run app/app.py
"""

import streamlit as st
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="California House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 1rem 0;
    }
    .prediction-value {
        font-size: 3rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model_and_preprocessor():
    """Load the trained model and preprocessor."""
    try:
        model = joblib.load("models/house_price_model.pkl")
        preprocessor = joblib.load("models/preprocessor.pkl")
        return model, preprocessor
    except FileNotFoundError:
        st.error("⚠️ Model files not found. Please train the model first by running the notebook.")
        return None, None


def create_input_features():
    """Create input features from user inputs."""
    # Location features
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📍 Location")
        longitude = st.slider(
            "Longitude",
            min_value=-125.0,
            max_value=-114.0,
            value=-122.0,
            step=0.01,
            help="How far west the property is (more negative = further west)"
        )
        latitude = st.slider(
            "Latitude",
            min_value=32.0,
            max_value=43.0,
            value=37.5,
            step=0.01,
            help="How far north the property is"
        )
        ocean_proximity = st.selectbox(
            "Ocean Proximity",
            options=["<1H OCEAN", "INLAND", "ISLAND", "NEAR BAY", "NEAR OCEAN"],
            help="Distance to the ocean"
        )
    
    with col2:
        st.markdown("### 🏠 Property Details")
        housing_median_age = st.slider(
            "Housing Median Age",
            min_value=1,
            max_value=52,
            value=25,
            help="Median age of houses in the block"
        )
        total_rooms = st.number_input(
            "Total Rooms",
            min_value=1,
            max_value=50000,
            value=2000,
            step=100,
            help="Total rooms in the census block"
        )
        total_bedrooms = st.number_input(
            "Total Bedrooms",
            min_value=1,
            max_value=10000,
            value=400,
            step=10,
            help="Total bedrooms in the census block"
        )
    
    # Population and income
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### 👥 Population")
        population = st.number_input(
            "Population",
            min_value=1,
            max_value=50000,
            value=1200,
            step=50,
            help="Total population in the census block"
        )
        households = st.number_input(
            "Households",
            min_value=1,
            max_value=10000,
            value=450,
            step=10,
            help="Number of households in the block"
        )
    
    with col4:
        st.markdown("### 💰 Income")
        median_income = st.slider(
            "Median Income ($10,000s)",
            min_value=0.5,
            max_value=15.0,
            value=3.5,
            step=0.1,
            help="Median household income in tens of thousands of dollars"
        )
    
    # Calculate engineered features
    rooms_per_household = total_rooms / max(households, 1)
    bedrooms_per_room = total_bedrooms / max(total_rooms, 1)
    population_per_household = population / max(households, 1)
    distance_to_sf = np.sqrt((latitude - 37.7749)**2 + (longitude - (-122.4194))**2)
    distance_to_la = np.sqrt((latitude - 34.0522)**2 + (longitude - (-118.2437))**2)
    income_per_room = median_income / max(rooms_per_household, 0.1)
    
    return {
        'longitude': longitude,
        'latitude': latitude,
        'housing_median_age': housing_median_age,
        'total_rooms': total_rooms,
        'total_bedrooms': total_bedrooms,
        'population': population,
        'households': households,
        'median_income': median_income,
        'ocean_proximity': ocean_proximity,
        'rooms_per_household': rooms_per_household,
        'bedrooms_per_room': bedrooms_per_room,
        'population_per_household': population_per_household,
        'distance_to_sf': distance_to_sf,
        'distance_to_la': distance_to_la,
        'income_per_room': income_per_room
    }


def predict_price(features, model, preprocessor):
    """Make prediction using the model."""
    input_df = pd.DataFrame([features])
    input_processed = preprocessor.transform(input_df)
    prediction = model.predict(input_processed)[0]
    return prediction


def create_map_visualization(features):
    """Create a map showing the property location."""
    fig = px.scatter_mapbox(
        lat=[features['latitude']],
        lon=[features['longitude']],
        zoom=8,
        height=400
    )
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":0,"l":0,"b":0}
    )
    return fig


def main():
    # Header
    st.markdown('<p class="main-header">🏠 California House Price Predictor</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Powered by Machine Learning | Predict home values across California</p>', unsafe_allow_html=True)
    
    # Load model
    model, preprocessor = load_model_and_preprocessor()
    
    if model is None or preprocessor is None:
        st.warning("👋 Welcome! To use this app, you need to train the model first.")
        st.info("Run the Jupyter notebook `notebooks/01_end_to_end_house_price_prediction.ipynb` to train and save the model.")
        return
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🎯 Predict", "📊 Insights", "ℹ️ About"])
    
    with tab1:
        st.markdown("### Enter Property Details")
        st.markdown("Adjust the sliders and inputs below to predict a house price.")
        
        # Get user inputs
        features = create_input_features()
        
        # Make prediction
        prediction = predict_price(features, model, preprocessor)
        
        # Display prediction
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f'''
                <div class="prediction-box">
                    <div style="font-size: 1.2rem; opacity: 0.9;">Predicted House Value</div>
                    <div class="prediction-value">${prediction:,.0f}</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">
                        Based on {features['ocean_proximity']} location
                    </div>
                </div>
            ''', unsafe_allow_html=True)
        
        # Show location on map
        st.markdown("### 📍 Property Location")
        map_fig = create_map_visualization(features)
        st.plotly_chart(map_fig, use_container_width=True)
        
        # Feature breakdown
        st.markdown("### 📊 Property Profile")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Rooms per Household", f"{features['rooms_per_household']:.1f}")
        with col2:
            st.metric("Bedroom Ratio", f"{features['bedrooms_per_room']:.2f}")
        with col3:
            st.metric("Population/Household", f"{features['population_per_household']:.1f}")
        with col4:
            st.metric("Income per Room", f"${features['income_per_room']*10000:.0f}")
    
    with tab2:
        st.markdown("### 📈 Model Insights")
        
        # Sample insights
        st.markdown("""
        <div class="info-box">
            <h4>🔍 What Drives California House Prices?</h4>
            <ul>
                <li><strong>Median Income</strong> is the strongest predictor - areas with higher incomes have more expensive homes</li>
                <li><strong>Ocean Proximity</strong> significantly affects prices - coastal properties command premiums</li>
                <li><strong>Location matters</strong> - Bay Area and coastal regions are most expensive</li>
                <li><strong>Room density</strong> - More rooms per household indicates more spacious (expensive) properties</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Price ranges by location
        st.markdown("### 🏖️ Typical Price Ranges by Location")
        
        price_data = {
            'Location': ['ISLAND', 'NEAR BAY', '<1H OCEAN', 'NEAR OCEAN', 'INLAND'],
            'Avg Price': [380000, 260000, 240000, 230000, 120000],
            'Description': [
                'Premium island properties',
                'Bay Area premium',
                'Coastal access',
                'Ocean nearby',
                'Interior regions'
            ]
        }
        
        fig = go.Figure(data=[
            go.Bar(
                x=price_data['Location'],
                y=price_data['Avg Price'],
                text=price_data['Description'],
                textposition='auto',
                marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
            )
        ])
        
        fig.update_layout(
            title='Average House Values by Ocean Proximity (1990 Census)',
            xaxis_title='Ocean Proximity',
            yaxis_title='Average House Value ($)',
            yaxis_tickformat='$,.0f',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tips
        st.markdown("""
        <div class="info-box">
            <h4>💡 Tips for Accurate Predictions</h4>
            <ul>
                <li>Higher median income typically means higher house values</li>
                <li>Properties near the ocean or bay are generally more expensive</li>
                <li>More rooms per household indicates more valuable properties</li>
                <li>The model was trained on 1990 census data - adjust expectations for current market!</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### ℹ️ About This Project")
        
        st.markdown("""
        #### 🎯 Project Overview
        
        This application uses machine learning to predict median house values in California 
        based on census data. The model was trained on the California Housing Dataset from 
        the 1990 census.
        
        #### 🤖 Machine Learning Pipeline
        
        1. **Data Preprocessing**: Missing value imputation, feature scaling, and encoding
        2. **Feature Engineering**: Created ratio features and distance metrics
        3. **Model Selection**: Compared Linear Regression, Ridge, Lasso, Random Forest, and Gradient Boosting
        4. **Hyperparameter Tuning**: Optimized the best performing model
        5. **Evaluation**: Achieved ~81% R² score on test data
        
        #### 🛠️ Technologies Used
        
        - **Python** - Core programming language
        - **Scikit-learn** - Machine learning library
        - **Pandas & NumPy** - Data manipulation
        - **Plotly** - Interactive visualizations
        - **Streamlit** - Web application framework
        
        #### 📊 Model Performance
        
        | Metric | Value |
        |--------|-------|
        | R² Score | ~0.81 |
        | RMSE | ~$45,000 |
        | MAE | ~$32,000 |
        
        #### 📝 Note
        
        This model predicts values based on 1990 census data. For current market values, 
        you would need to adjust for inflation (approximately 2.5x increase) and current 
        market conditions.
        
        ---
        
        **Created with ❤️ using Python & Machine Learning**
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666;'>"
        "Made with Streamlit | California Housing Price Prediction Project"
        "</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
