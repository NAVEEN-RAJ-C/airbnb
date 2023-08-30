import pandas as pd
from streamlit_folium import folium_static
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import folium
import ast


def main():
    st.set_page_config(page_title='Airbnb Analysis', layout='wide')
    df = pd.read_csv('airbnb.csv')
    st.title('Airbnb Listing Geo-visualisation')
    if st.button("Get Geomapping"):
        df = df.sample(n=100, random_state=42)
        m = folium.Map(location=[0, 0], zoom_start=4)

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

    st.title('Graphical Analysis')
    # Convert Decimal128 to float64 for visualization
    df['price'] = df['price'].apply(lambda x: float(str(x)))
    category = st.selectbox('Select a category', ['None', 'property_type', 'room_type', 'bed_type', 'country'])
    if category != 'None':
        # Set Seaborn style
        sns.set(style="whitegrid")

        # Create a bar plot using Seaborn
        plt.figure(figsize=(8, 6))
        sns.barplot(x=category, y='price', data=df)
        plt.xlabel(category)
        plt.ylabel('price')
        plt.title('Price Distribution')
        plt.xticks(rotation=90)

        # Display Seaborn plot using st.pyplot
        st.pyplot()


if __name__ == "__main__":
    main()
