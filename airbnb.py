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
    if st.button('Show'):
        if category != 'None':
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

    st.title('Heatmap')
    if st.button('Show Heatmap'):
        # Select the relevant columns for the heatmap
        columns_to_visualize = ['price', 'monthly_price', 'bedrooms', 'reviews_per_month', 'maximum_nights']

        # Create a pivot table or reshape the data if needed
        # Example: pivot_table = df.pivot_table(index='name', columns='roomtype', values='price', aggfunc='mean')

        # Create a heatmap using Seaborn
        fig, ax = plt.subplots(figsize=(12, 10))
        heatmap_data = df[columns_to_visualize].corr()
        sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt='.2f', ax=ax)
        plt.title('Heatmap of Column Relationships')

        # Display Matplotlib figure using st.pyplot
        st.pyplot(fig)
        plt.close(fig)  # Close the figure to release resources

    st.title('Price Table')
    country = st.selectbox('Select a country', df['country'].unique())
    roomtype = st.selectbox('Select a roomtype', df['room_type'].unique())
    bedrooms = st.selectbox('Select number of bedrooms', df['bedrooms'].unique())
    if st.button('show table'):
        # Filter the DataFrame based on user selections
        filtered_df = df[(df['country'] == country) & (df['room_type'] == roomtype) & (df['bedrooms'] == bedrooms)]

        # Select specific columns to display from the filtered DataFrame
        columns_to_display = ['name', 'price', 'availability', 'reviews_per_month', 'maximum_nights']
        # Display the filtered DataFrame
        st.write(filtered_df[columns_to_display])


if __name__ == "__main__":
    main()
