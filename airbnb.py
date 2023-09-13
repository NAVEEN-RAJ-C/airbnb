import pandas as pd
from streamlit_folium import folium_static
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import folium
import ast


def is_valid_availability(avail_dict):
    # Define the expected keys for valid availability dictionaries
    expected_keys = ['availability_30', 'availability_60', 'availability_90', 'availability_365']

    # Check if the keys in the dictionary match the expected keys
    return all(key in avail_dict for key in expected_keys)


def geomap(df):
    m = folium.Map(zoom_start=4)

    # Add markers with tooltips to the map
    for index, row in df.iterrows():
        lon, lat = ast.literal_eval(row['coordinates'])
        tooltip_content = f"Name: {row['name']}<br>Country: {row['country']}<br>Price: {row['price']}" \
                          f"<br>Weekly_Price: {row['weekly_price']}<br>Monthly_Price: {row['monthly_price']}"

        folium.Marker(
            location=[lat, lon],
            tooltip=folium.Tooltip(tooltip_content, sticky=True)  # Display tooltip on hover
        ).add_to(m)

    # Display Folium map in Streamlit
    folium_static(m, width=800, height=600)


def graph(df, category):
    # Convert Decimal128 to float64 for visualization
    df['price'] = df['price'].apply(lambda x: float(str(x)))
    # Set Seaborn style
    sns.set(style="whitegrid")

    # Create a bar plot using Seaborn
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=category, y='price', data=df, ax=ax)
    ax.set_xlabel(category)
    ax.set_ylabel('price')
    ax.set_title('Price Distribution')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

    # Display Matplotlib figure using st.pyplot
    st.pyplot(fig)
    plt.close(fig)  # Close the figure to release resources


def heat(df):
    # Select the relevant columns for the heatmap
    columns_to_visualize = ['price', 'monthly_price', 'bedrooms', 'reviews_per_month', 'maximum_nights',
                            'accommodates', 'beds', 'number_of_reviews', 'bathrooms', 'security_deposit',
                            'cleaning_fee', 'extra_people', 'guests_included', 'availability_30',
                            'availability_60', 'availability_90', 'availability_365', 'rating']

    # Create a heatmap using Seaborn
    fig, ax = plt.subplots(figsize=(10, 10))
    heatmap_data = df[columns_to_visualize].corr()
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt='.2f', ax=ax)
    plt.title('Heatmap of Column Relationships')

    # Display Matplotlib figure using st.pyplot
    st.pyplot(fig)
    plt.close(fig)  # Close the figure to release resources


def price_table(df, roomtype, bedrooms):
    # Filter the DataFrame based on user selections
    filtered_df = df[(df['room_type'] == roomtype) & (df['bedrooms'] == bedrooms)]

    # Select specific columns to display from the filtered DataFrame
    columns_to_display = ['name', 'price', 'reviews_per_month', 'maximum_nights', 'availability_30',
                          'availability_60', 'availability_90', 'availability_365']
    # Sort the DataFrame by the 'price' column in ascending order
    sorted_df = filtered_df.sort_values(by='price', ascending=True)

    # Display the sorted DataFrame
    st.write(sorted_df[columns_to_display])


def main():
    # read the csv file
    df = pd.read_csv('airbnb.csv')
    st.set_page_config(page_title='Airbnb Analysis', layout='wide')
    # Use Markdown with HTML/CSS to center-align the title
    st.markdown('<h1 style="text-align: center;">AIRBNB ANALYSIS</h1>', unsafe_allow_html=True)
    st.header('Airbnb Listing Geo-visualisation')
    country = st.sidebar.selectbox('Select a country', df['country'].unique())
    df = df[(df['country'] == country)]
    # Geographical analysis of the listings
    geomap(df)

    # Heatmap to find co-relation
    st.header('Heatmap')
    heat(df)
    # Graphical representation
    st.header('Graphical Analysis')
    category = st.selectbox('Select a category', ['property_type', 'room_type', 'bed_type'])
    if category != 'None':
        graph(df, category)

    # Price table for selected features
    st.header('Price Table')
    roomtype = st.selectbox('Select a roomtype', df['room_type'].unique())
    bedrooms = st.selectbox('Select number of bedrooms', df['bedrooms'].unique())
    price_table(df, roomtype, bedrooms)


if __name__ == "__main__":
    main()
