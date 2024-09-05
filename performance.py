import streamlit as st
import pandas as pd
import plotly.express as px

def create_performance_bar_chart(data, x, y, title, color, range_y):
    fig = px.bar(data, x=x, y=y, title=title, text=y, labels={x: ''})
    fig.update_traces(marker_color=color, textposition='outside')
    fig.update_yaxes(range=range_y, tickformat='.3f' if y == 'R²' else '.0f', title=y) # Add y-axis title
    fig.update_xaxes(title='Model')  # Add x-axis title
    # Add hover data (optional)
    fig.update_traces(hovertemplate='Model: %{x}<br>' + y + ': %{y}') 
    return fig

# chart values (converted to DataFrame)
data = pd.DataFrame({
    'Model': ['Random Forest', 'XGBoost', 'Ridge Regression', 'ARIMA', 'Prophet'],
    'MSE': [3837.18, 3706.97, 23075.96, 21952.13, 28386.89],
    'MAE': [48.36, 42.1, 123.58, 121.29, 140.25],
    'R²': [0.9956, 0.9957, 0.9735, 0.9748, 0.9674]
})

# chart colors
COLORS = {
    'MSE' : '#4c4cff',
    'MAE' : '#4ca64c',
    'R²' : '#ff4b4c'
}

def display_performance():
    st.header("Model Performance")


    # Add metric definitions (optional)
    st.markdown("""
    * **MSE (Mean Squared Error):** Measures the average squared difference between the predicted values and the actual values. Lower MSE indicates better performance
    * **MAE (Mean Absolute Error):** Measures the average absolute difference between the predicted values and the actual values
    * **R² (R-squared):** Represents the proportion of variance in the dependent variable that is explained by the independent variables. Higher R² indicates better performance.
    """)

    col1, col2 = st.columns(2)
    col1.plotly_chart(create_performance_bar_chart(data, 'Model', 'MSE', 'Mean Squared Error Comparison', COLORS['MSE'], [0, 30000]))
    col2.plotly_chart(create_performance_bar_chart(data, 'Model', 'MAE', 'Mean Absolute Error Comparison', COLORS['MAE'], [0, 150]))
    col1, col2, col3 = st.columns([1,2,1])
    col2.plotly_chart(create_performance_bar_chart(data, 'Model', 'R²', 'R-squared Comparison', COLORS['R²'], [0.965, 1]))


    