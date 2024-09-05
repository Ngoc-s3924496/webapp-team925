import streamlit as st
import pandas as pd 

@st.cache_data 
def display_roadmap():
    st.header("AI Adoption Roadmap")

    # Data for the table
    data = {
        'Items': ['Setup sensors', 'Collect data', 'Model implementation', 'Hyperparameters Tuning', 'User interface', 'Integration'],
        'Duration (Weeks)': ['4', '104 (2 years)', '2', '4', '2', '1'],
        'Objective': [
            'Sensors for measuring environmental factors',
            'Collect data for training models.',
            'This step is to implement the machine learning models in code.',
            'This step is to tune the hyperparameters of the model to reach the best performance.',
            'This step is to develop the user interface to show the data and the model performance.',
            'This step is to integrate between the user interface and the fine-tuned models.'
        ]
    }

    # Create the DataFrame
    df = pd.DataFrame(data)

    # Styling the table using CSS
    st.markdown(
    f"""
    <style>
    table th:first-child {{
        background-color: blue;
        color: white; /* Adjust text color if needed */
    }}
    table tr:first-child th {{
        background-color: red;
        color: white; /* Adjust text color if needed */
    }}
    .centered-table {{
        margin: 0 auto; /* Center the table horizontally */
        width: 80%; /* Adjust width as needed */
    }}
    </style>
    """, 
    unsafe_allow_html=True
    )

    # Display the table 
    st.write(df.to_markdown(index=False, numalign="left", stralign="left"), unsafe_allow_html=True)

# Call the function to display the roadmap
display_roadmap()