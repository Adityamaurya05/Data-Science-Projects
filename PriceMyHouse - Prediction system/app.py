import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

st.set_page_config(page_title="India House Price Predictor", layout="wide")

try:
    model = pickle.load(open('model.pkl', 'rb'))
    df = pd.read_csv('House Price India.csv')
    
    df.columns = df.columns.str.strip().str.lower()
    
    column_mapping = {
        'living_area': 'area of the house(excluding basement)',
        'lot_area': 'lot area',
        'bedrooms': 'number of bedrooms',
        'bathrooms': 'number of bathrooms',
        'floors': 'number of floors',
        'condition': 'condition of the house',
        'grade': 'grade of the house',
        'built_year': 'built year',
        'postal_code': 'postal code',
        'latitude': 'lattitude',
        'longitude': 'longitude',
        'schools': 'number of schools nearby',
        'airport_dist': 'distance from the airport'
    }
    
except Exception as e:
    st.error(f"Failed to load model or dataset: {str(e)}")
    st.stop()

# Title and description
st.title("🏡 India House Price Prediction")
st.markdown("""
Predict the market value of residential properties across India based on key features.
Adjust the parameters below and click **Predict Price**.
""")

with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Property Details")
        living_area = st.number_input("Living Area (sqft)",
            min_value=int(df[column_mapping['living_area']].min()), 
            max_value=int(df[column_mapping['living_area']].max()), 
            value=1500)

        lot_area = st.number_input("Lot Area (sqft)", 
            min_value=int(df[column_mapping['lot_area']].min()), 
            max_value=int(df[column_mapping['lot_area']].max()), 
            value=5000)

        bedrooms = st.slider("Number of Bedrooms", 
            min_value=int(df[column_mapping['bedrooms']].min()), 
            max_value=int(df[column_mapping['bedrooms']].max()), 
            value=3)

        bathrooms = st.slider("Number of Bathrooms", 
            min_value=int(df[column_mapping['bathrooms']].min()), 
            max_value=int(df[column_mapping['bathrooms']].max()), 
            value=2)

        floors = st.slider("Number of Floors", 
            min_value=int(df[column_mapping['floors']].min()), 
            max_value=int(df[column_mapping['floors']].max()), 
            value=1)

    with col2:
        st.subheader("Quality Assessment")
        condition = st.selectbox("House Condition",
            options=sorted(df[column_mapping['condition']].unique()),
            format_func=lambda x: f"{x} ({['Poor', 'Fair', 'Average', 'Good', 'Excellent'][x-1]})")

        grade = st.selectbox("Construction Grade",
            options=sorted(df[column_mapping['grade']].unique()),
            help="Quality of construction (higher = better)")

        built_year = st.slider("Year Built", 
            min_value=int(df[column_mapping['built_year']].min()), 
            max_value=int(df[column_mapping['built_year']].max()), 
            value=2000)

    with col3:
        st.subheader("Location Details")
        postal_code = st.selectbox("Postal Code", sorted(df[column_mapping['postal_code']].unique()))

        lat_min, lat_max = float(df[column_mapping['latitude']].min()), float(df[column_mapping['latitude']].max())
        lon_min, lon_max = float(df[column_mapping['longitude']].min()), float(df[column_mapping['longitude']].max())

        latitude = st.slider("Latitude", 
            min_value=lat_min, max_value=lat_max, value=(lat_min + lat_max) / 2)

        longitude = st.slider("Longitude", 
            min_value=lon_min, max_value=lon_max, value=(lon_min + lon_max) / 2)

        st.subheader("Neighborhood")
        schools = st.slider("Number of Schools Nearby", 
            min_value=int(df[column_mapping['schools']].min()), 
            max_value=int(df[column_mapping['schools']].max()), 
            value=5)

        airport_dist = st.number_input("Distance from Airport (km)", 
            min_value=float(df[column_mapping['airport_dist']].min()), 
            max_value=float(df[column_mapping['airport_dist']].max()), 
            value=50.0)
    
    submitted = st.form_submit_button("Predict Price")

if submitted:
    try:
        
        input_data = {
            'Area of the house(excluding basement)': living_area,
            'Lot area': lot_area,
            'number of bedrooms': bedrooms,
            'number of bathrooms': bathrooms,
            'number of floors': floors,
            'condition of the house': condition,
            'grade of the house': grade,
            'Built Year': built_year,
            'Postal Code': postal_code,
            'Lattitude': latitude,
            'Longitude': longitude,
            'Number of schools nearby': schools,
            'Distance from the airport': airport_dist
        }
        
        input_df = pd.DataFrame([input_data])
        
        for feature in model.feature_names_in_:
            if feature not in input_df.columns:
                input_df[feature] = 0 
        
        input_df = input_df[model.feature_names_in_]
        
        prediction = model.predict(input_df)[0]
        
        st.success(f"""
        ## Predicted Property Value: ₹{prediction:,.2f}
        (Approximately ₹{prediction/100000:,.2f} lakhs)
        """)
        
        if hasattr(model, 'feature_importances_'):
            st.subheader("Key Price Factors")
            importance_df = pd.DataFrame({
                'Feature': model.feature_names_in_,
                'Importance': model.feature_importances_
            }).sort_values('Importance', ascending=False)
            
            st.dataframe(importance_df.head(10), hide_index=True)
            
    except Exception as e:
        st.error(f"Prediction failed: {str(e)}")
        st.write("Model expects:", model.feature_names_in_)
        st.write("You provided:", input_df.columns if 'input_df' in locals() else "No input data")

