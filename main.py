import streamlit as st
from streamlit_option_menu import option_menu

# Import your page modules
from data import display_data
from chart import display_chart
from prediction import display_prediction
from performance import display_performance
from roadmap import display_roadmap

# Sidebar Menu
with st.sidebar:
    # Display the logo (replace 'your_logo.png' with your actual logo file)

    selected = option_menu(
        menu_title="Main Menu",
        options=["Data Table", "Data Visualization", "Body Weight Prediction", "Model Performance", "AI Adoption Roadmap"],
        menu_icon="cast",
        default_index=0,
    )

# Initialize session state variable if it doesn't exist
if 'page' not in st.session_state:
    st.session_state.page = "Data"  # Default to Data page

# Update session state based on the selected option
if selected == "Data Table":
    st.session_state.page = "data"
elif selected == "Data Visualization":
    st.session_state.page = "visualization"
elif selected == "Body Weight Prediction":
    st.session_state.page = "prediction"
elif selected == "Model Performance":
    st.session_state.page = "performance"
elif selected == "AI Adoption Roadmap":
    st.session_state.page = "roadmap"

# Main content area
if st.session_state.page == "data":
    display_data() 

elif st.session_state.page == "visualization":
    display_chart()

elif st.session_state.page == "prediction":
    display_prediction()

elif st.session_state.page == "performance":
    display_performance()

elif st.session_state.page == "roadmap":
    display_roadmap()
