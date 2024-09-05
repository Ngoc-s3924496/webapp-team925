import streamlit as st
import pandas as pd
import pickle
import os

print(os.getcwd())  
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

    # Input fields for user with validation
    avgtemp_c = st.number_input('Average Temperature (°C)', min_value=-20, max_value=50)
    avghumidity = st.number_input('Humidity (%)', min_value=0, max_value=100)
    age = st.number_input('Age (Days)', min_value=0)
    feedintake = st.number_input('Feed Intake (gm/bird/day)', min_value=0)

    # Predict button
    if st.button('Predict Weight'):
        try:
            # Create input DataFrame - make sure feature names match training data
            input_data = pd.DataFrame({
                'avgtemp_c': [avgtemp_c],
                'avghumidity': [avghumidity],
                'age': [age],  
                'feedintake': [feedintake]  
            })

            # Get the model for the selected location
            model = models[location]

            # Make prediction
            prediction = model.predict(input_data)

            # Display prediction with location context
            st.success(f'Predicted Broiler Weight in {location}: {prediction[0]:.2f} grams')
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Run the app
if __name__ == "__main__":
    display_prediction()
