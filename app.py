import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
@st.cache_resource
def load_data():
    return pd.read_csv('nco2.csv')

data = load_data()

# Sidebar - User Inputs
st.sidebar.header('Select Features')

# Select Insight
insight_choices = {
    'CO2 Emissions': 'CO2_Emissions_g_km_',
    'Fuel Consumption Combined': 'Fuel_Consumption_Comb__L_100_km_',
    'Fuel Consumption City': 'Fuel_Consumption_City__L_100_km_',
    'Fuel Consumption Highway': 'Fuel_Consumption_Hwy__L_100_km_'
}
insight = st.sidebar.selectbox('Select Insight:', list(insight_choices.keys()))

# Select Graph Type
graph_types = ['Bar Graph', 'Histogram', 'Scatter Plot', 'Box Plot']
graph_type = st.sidebar.selectbox('Select Graph Type:', graph_types)

# Based on the selected graph type, enable or disable the attribute selection
is_attribute_selection_enabled = graph_type != 'Histogram'

# Select attribute for analysis - X-axis
attributes = ['Make', 'Transmission', 'Engine_Size_L_', 'Cylinders', 'Model'] if is_attribute_selection_enabled else ['N/A']
attribute = st.sidebar.selectbox('Select Attribute for X-axis:', attributes, disabled=not is_attribute_selection_enabled)

# If 'Model' is the attribute, handle the logic for selecting a make and models
if attribute == 'Model':
    selected_make = st.sidebar.selectbox('Select Make for Model Analysis:', sorted(data['Make'].unique().tolist()))
    data = data[data['Make'] == selected_make]
    model_options = sorted(data['Model'].unique().tolist())
    selected_models = st.sidebar.multiselect('Select Model(s):', model_options)
    if not selected_models:
        st.error('Please select at least one model.')
        st.stop()
    data = data[data['Model'].isin(selected_models)]


# Determine if the attribute selection is relevant for the chosen graph type
is_attribute_relevant = graph_type in ['Bar Graph', 'Scatter Plot','Box Plot']

# Format the title based on the selections
if is_attribute_relevant:
    title_text = f"{graph_type} for {insight} by {attribute}"
else:
    title_text = f"{graph_type} for {insight}"

st.title(title_text)

# Plotting function
def plot_graph(data, x_attribute, y_attribute, graph_type):
    fig, ax = plt.subplots(figsize=(10, 5))
    if graph_type == 'Bar Graph':
        sns.barplot(x=x_attribute, y=y_attribute, data=data, ax=ax)
    elif graph_type == 'Histogram':
        sns.histplot(data[data[y_attribute].notnull()][y_attribute], kde=True, bins=30, ax=ax)
    elif graph_type == 'Scatter Plot':
        sns.scatterplot(x=x_attribute, y=y_attribute, data=data, ax=ax)
    elif graph_type == 'Box Plot':
        sns.boxplot(x=x_attribute, y=y_attribute, data=data, ax=ax)

    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(fig)

# For histograms, use the insight choice directly without an X-axis attribute
if graph_type == 'Histogram':
    plot_graph(data, 'N/A', insight_choices[insight], graph_type)
else:
    plot_graph(data, attribute, insight_choices[insight], graph_type)


