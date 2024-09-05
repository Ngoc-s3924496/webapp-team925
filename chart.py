import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Helper functions (moved outside display_chart)
def read_excel_file(file_path):
    try:
        df = pd.read_excel(file_path, sheet_name='Sheet1')
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return None
    except pd.errors.ParserError:
        st.error("Error parsing the file. Please check the file format.")
        return None

# Colors
COLORS = {"default" : "#85c7fd","temperature" : "#1790a7", "humidity" : "#9bcfa9", 
        "precipitation" : "#0000FF", "uv" : "#FFFF00", "bodyweight": "#f4671e", "feedintake": "#ffaf01"} 
    
def line_bydate_fig(df, column_name, column_label, title, line_color=COLORS['default']):
        # Plot using Plotly
        fig = px.line(
            df,
            x=df['date'],
            y=column_name,
            labels={column_name: column_label, 'date': 'Date'},
            title= title
        )
        # Select the first day of each month for tick values
        tickvals = df[df['date'].dt.is_month_start]['date']
        # Get the corresponding month names for tick labels
        ticktext = tickvals.dt.strftime('%B')
        # Update x-axis to show month names at the start of each month
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=tickvals,
                ticktext=ticktext
            )
        )
        # Update line color
        fig.update_traces(line=dict(color=line_color))
        return fig

def histogram_fig(df, column_name,column_label,title, color=COLORS['default']):
    fig = px.histogram(df, x=column_name, nbins=40, title=title, labels={column_name: column_label}, color_discrete_sequence=[color])
    fig.update_layout(bargap=0.15)
    return fig

def scatter_byage_fig(df, column_name, column_label, title, color=COLORS['default']):
    fig = px.scatter(df, x='age(day)', y=column_name,
                    title=title,
                    labels={'age(day)': 'Age (days)', column_name: column_label},
                    color_discrete_sequence=[color],
                    hover_data={'Date': True})
    fig.update_traces(marker=dict(symbol='x',size=9))
    return fig

def doubleline_byage_fig(df,col1_name, col2_name, title):
    # Calculate the mean feed intake and bodyweight by age
    mean_data = df.groupby('age(day)')[[col1_name, col2_name]].mean().reset_index()
    fig = px.line(mean_data, 
                x='age(day)', 
                y=[col1_name, col2_name], 
                labels={'age(day)': 'Age (days)', 
                        'value': 'Mean Values'},
                title=title,
                color_discrete_map={'feedintake (gm/bird/day)': COLORS['feedintake'], 'bodyweight (gm/bird)': COLORS['bodyweight']})
    # Adding markers to the plot
    fig.update_traces(mode='lines+markers')
    return fig

def display_chart():
    def read_excel_file(file_path):
        df = pd.read_excel(file_path, sheet_name='Sheet1')
        # Convert 'date' column to datetime format
        df['date'] = pd.to_datetime(df['date'])
        return df

    # Load  data (adjust the file path as necessary)
    file_path = 'Rounded_Farm_Data_with_Weather_Data.xlsx'
    data = read_excel_file(file_path)

    # List of available locations and years
    location = data['location'].unique()
    year = data['date'].dt.year.unique()

    # show UI
    st.title("Data Visualization")
    tab1, tab2, tab3 = st.tabs(["Annual Environmental Data", "Data Distribution","Data Correlation"])

    # TAB 1: Annual Environmental Data
    with tab1:
        st.markdown("<h2 style='text-align: center'>Annual Environmental Data</h2>", unsafe_allow_html=True)

        container = st.container(border=True)
        col1, col2, col3 = st.columns([1, 2, 1]) # center container
        # Filter data for a specific location and year
        centered_container = col2.container(height=190)
        location_filter = centered_container.selectbox('Select a location', location)
        year_filter = centered_container.selectbox('Select a year', year)
        filtered_data = data[(data['location'] == location_filter) & (data['date'].dt.year == year_filter)]
        # plot charts
        col1, col2 = st.columns(2)
        col1.plotly_chart(line_bydate_fig(filtered_data, 'avgtemp_c','Temperature (°C)','Daily Temperature',COLORS['temperature']))
        col1.plotly_chart(line_bydate_fig(filtered_data, 'avghumidity','Humidity (%)','Daily Humidity',COLORS['humidity']))
        col2.plotly_chart(line_bydate_fig(filtered_data, 'totalprecip_mm','Precipitation (mm)','Daily Precipitation',COLORS['precipitation']))
        col2.plotly_chart(line_bydate_fig(filtered_data, 'uv','UV index','Daily UV',COLORS['uv']))

    # TAB 2: Data Distribution
    with tab2:
        st.markdown("<h2 style='text-align: center'>Data Distribution</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        col1.plotly_chart(histogram_fig(data, 'avgtemp_c', 'Temperature (°C)','Temperature',COLORS['temperature']))
        col2.plotly_chart(histogram_fig(data, 'avghumidity', 'Humidity (%)','Humidity',COLORS['humidity']))
        col1.plotly_chart(histogram_fig(data, 'totalprecip_mm', 'Precipitation (mm)','Precipitation',COLORS['precipitation']))
        col2.plotly_chart(histogram_fig(data, 'uv','UV Index', 'UV',COLORS['uv']))
        col1.plotly_chart(histogram_fig(data, 'feedintake (gm/bird/day)', 'Feed Intake (gm/bird/day)','Feed Intake',COLORS['feedintake']))
        col2.plotly_chart(histogram_fig(data, 'bodyweight (gm/bird)', 'Body Weight (gm/bird)','Body Weight',COLORS['bodyweight']))
        col1, col2, col3 = st.columns([1, 2, 1]) # center 7th chart
        col2.plotly_chart(histogram_fig(data, 'age(day)', 'Age (days)','Age'))

    # TAB 3: Data Correlation
    with tab3: 
        st.markdown("<h2 style='text-align: center'>Data Correlation</h2>", unsafe_allow_html=True)
        data['Date'] = data['date'].dt.strftime('%b %d, %Y') # format date to MMM DD, YYYY

        # plot charts
        col1, col2 = st.columns(2)
        col1.plotly_chart(scatter_byage_fig(data, 'bodyweight (gm/bird)', 'Body Weight (gm/bird)', 'Correlation between Body Weight and Age'))
        col2.plotly_chart(scatter_byage_fig(data, 'feedintake (gm/bird/day)', 'Feed Intake (gm/bird/day)', 'Correlation between Feed Intake and Age'))
        st.plotly_chart(doubleline_byage_fig(data,'bodyweight (gm/bird)','feedintake (gm/bird/day)','Mean Body Weight and Feed Intake Grouped By Age'))
