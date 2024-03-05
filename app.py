import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_resource
def load_data():
    return pd.read_csv('nco2.csv')


data = load_data()


st.sidebar.header('Select Features')


insight_choices = {
    'CO2 Emissions': 'CO2_Emissions_g_km_',
    'Fuel Consumption Combined': 'Fuel_Consumption_Comb__L_100_km_',
    'Fuel Consumption City': 'Fuel_Consumption_City__L_100_km_',
    'Fuel Consumption Highway': 'Fuel_Consumption_Hwy__L_100_km_'
}
insight = st.sidebar.selectbox('Select Insight:', list(insight_choices.keys()))


graph_types = ['Bar Graph', 'Histogram', 'Scatter Plot', 'Box Plot', 'Violin Plot']
graph_type = st.sidebar.selectbox('Select Graph Type:', graph_types)


is_attribute_selection_enabled = graph_type != 'Histogram'


attributes = ['Make', 'Transmission', 'Engine_Size_L_', 'Cylinders',
              'Model'] if is_attribute_selection_enabled else ['N/A']
attribute = st.sidebar.selectbox('Select Attribute for X-axis:', attributes,
                                 disabled=not is_attribute_selection_enabled)


if attribute == 'Model':
    selected_make = st.sidebar.selectbox('Select Make for Model Analysis:',
                                         sorted(
                                             data['Make'].unique().tolist()))
    data = data[data['Make'] == selected_make]
    model_options = sorted(data['Model'].unique().tolist())
    selected_models = st.sidebar.multiselect('Select Model(s):', model_options)
    if not selected_models:
        st.error('Please select at least one model.')
        st.stop()
    data = data[data['Model'].isin(selected_models)]


title_text = f"{graph_type} for {insight} by {attribute}" if is_attribute_selection_enabled else f"{graph_type} for {insight}"
st.title(title_text)


# Plotting function using Plotly
def plot_graph(data, x_attribute, y_attribute, graph_type):
    color_continuous_scale = px.colors.sequential.Viridis
    color_discrete_sequence = px.colors.qualitative.Set2

    if graph_type == 'Bar Graph':
        fig = px.bar(data, x=x_attribute, y=y_attribute, title=title_text,
                     color=x_attribute,
                     color_continuous_scale=color_continuous_scale)
    elif graph_type == 'Histogram':
        fig = px.histogram(data, x=y_attribute, nbins=30, title=title_text,
                           color_discrete_sequence=color_discrete_sequence)
    elif graph_type == 'Scatter Plot':
        fig = px.scatter(data, x=x_attribute, y=y_attribute, title=title_text,
                         color=x_attribute,
                         color_continuous_scale=color_continuous_scale)
    elif graph_type == 'Box Plot':
        fig = px.box(data, x=x_attribute, y=y_attribute, title=title_text,
                     color=x_attribute,
                     color_discrete_sequence=color_discrete_sequence)

    elif graph_type == 'Violin Plot':
        fig = px.violin(data, x=x_attribute, y=y_attribute, box=True,
                        points="all",color=x_attribute,
                        title=f"{graph_type} for {y_attribute} by {x_attribute}")

    st.plotly_chart(fig, use_container_width=True)

# Execute plotting
if graph_type == 'Histogram':
    plot_graph(data, 'N/A', insight_choices[insight], graph_type)
else:
    plot_graph(data, attribute, insight_choices[insight], graph_type)
