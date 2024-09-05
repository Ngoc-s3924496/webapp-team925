import streamlit as st
import pandas as pd
import pickle

# Load your XGBoost models (assuming you have them saved in separate files)
models = {
    'Bago': pickle.load(open('xgboost_Bago_model.pkl', 'rb')),
    'Hmawbi': pickle.load(open('xgboost_Hmawbi_model.pkl', 'rb')),
    'Kamase': pickle.load(open('xgboost_Kamase_model.pkl', 'rb')),
    'Mezali': pickle.load(open('xgboost_Mezali_model.pkl', 'rb')),
    'Taungnyo': pickle.load(open('xgboost_Taungnyo_model.pkl', 'rb'))
}

def display_prediction():
    st.header("Body Weight Prediction")

    # Dropdown for location selection
    location = st.selectbox('Select Location', list(models.keys()))

    # Input fields for user
    avgtemp_c = st.number_input('Average Temperature (°C)')
    avghumidity =  st.number_input ('Humidity (%)')
    age = st.number_input('Age (Days)')
    feedintake = st.number_input('Feed Intake (gm/bird/day)')

    # Predict button
    if st.button('Predict Weight'):
    # Create input DataFrame - make sure feature names match training data
        input_data = pd.DataFrame({
        'avgtemp_c': [avgtemp_c],
        'avghumidity': [avghumidity],
        'age': [age],  # Match the training data name
        'feedintake': [feedintake]  # Match the training data name
        })

        # Get the model for the selected location
        model = models[location]

        # Make prediction
        prediction = model.predict(input_data)

        # Display prediction
        st.success(f'Predicted Broiler Weight: {prediction[0]:.2f} grams')
