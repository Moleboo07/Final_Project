"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from geopy.geocoders import Nominatim


st.set_page_config(page_title="Service-publics", page_icon=":books:", layout="wide")

st.title("Services publics")


selected_tab = st.sidebar.selectbox("Sélectionner un onglet", ("global", "pole emploi"))

# Charger les données depuis le fichier CSV
df = pd.read_csv("export-experiences.csv", sep=";")
df[['Date', 'Heure']] = df['Date de publication'].str.split('T',n=1, expand=True)
df['Date'] = pd.to_datetime(df['Date'])
df['Mois'] = df['Date'].dt.to_period('M')
if selected_tab == "global":
    st.header('Ce qui se dit sur la plateforme SP+')

    services = df['Intitulé Typologie 1'].unique()
    service = st.multiselect('Service', services, key="service_multiselect")
    regions = df['Intitulé région usager'].unique()
    region = st.multiselect('Région', regions, key="region_multiselect")
    departements = df['Intitulé département usager'].unique()
    departement = st.multiselect('Département', departements, key="departement_multiselect")
    
   

    option_mapping = {
            # 'concours_1': 'concours',
            'service': 'Intitulé Typologie 1',
            'region': 'Intitulé région usager',
            'departement': 'Intitulé département usager'

        }

    query = df
    # loop over the options and add conditions to the query as needed
    for option, column in option_mapping.items():
        if len(eval(option)) > 0:
            query = query[query[column].isin(eval(option))]

        # set the filtered_data variable to the final query result
    filtered_data = query
    #  # Dates de début et de fin
    # start_date = df['Date'].min().date()
    # end_date = df['Date'].max().date()

    # # Sélection de la plage de dates avec un select_slider
    # selected_dates = st.slider("Sélectionnez une plage de dates", start_date, end_date, (start_date, end_date))

    # # Filtrer le DataFrame en fonction des dates sélectionnées
    # start_selected_date, end_selected_date = selected_dates
    # start_selected_date = pd.to_datetime(selected_dates[0])
    # end_selected_date = pd.to_datetime(selected_dates[1])
    # filtered_data = df.loc[df['Date'].between(start_selected_date, end_selected_date)]
    # Afficher le DataFrame filtré
    st.write(filtered_data)
    st.subheader("Nombre total d'avis en 2019, 2020, 2021 et 2022")

        
    #Combien d'avis ont été posté en 2019 ? 
    filtered_data['Date'] = pd.to_datetime(filtered_data['Date'])
    avis_2019 = filtered_data[filtered_data['Date'].dt.year == 2019].groupby('Date')['ID expérience'].value_counts()

    avis_2019 = avis_2019.sum()

    print(avis_2019)


    #Nombre d'avis par mois 2019 
    avis_par_mois_2019 = filtered_data[filtered_data['Date'].dt.year == 2019].set_index('Date')['ID expérience'].resample('M').count()

    # Afficher les résultats
    print(avis_par_mois_2019)


    #Combien d'avis ont été posté en 2020 ? 
    avis_2020 = filtered_data[filtered_data['Date'].dt.year == 2020].groupby('Date')['ID expérience'].value_counts()

    avis_2020 = avis_2020.sum()

    print(avis_2020)

    #Nombre d'avis par mois 2020
    avis_par_mois_2020 = filtered_data[filtered_data['Date'].dt.year == 2020].set_index('Date')['ID expérience'].resample('M').count()

    # Afficher les résultats
    print(avis_par_mois_2020)




    #Combien d'avis ont été posté en 2021 ? 
    avis_2021 = filtered_data[filtered_data['Date'].dt.year == 2021].groupby('Date')['ID expérience'].value_counts()

    avis_2021 = avis_2021.sum()

    print(avis_2021)

    #Nombre d'avis par mois 2019 
    avis_par_mois_2021 = filtered_data[filtered_data['Date'].dt.year == 2021].set_index('Date')['ID expérience'].resample('M').count()

    # Afficher les résultats
    print(avis_par_mois_2021)


    #Combien d'avis ont été posté en 2022 ? 
    avis_2022 = filtered_data[filtered_data['Date'].dt.year == 2022].groupby('Date')['ID expérience'].value_counts()

    avis_2022 = avis_2022.sum()

    print(avis_2022)

    #Nombre d'avis par mois 2019 
    avis_par_mois_2022 = filtered_data[(filtered_data['Date'].dt.year == 2022) & (filtered_data['Date'].dt.month >= 1) & (filtered_data['Date'].dt.month <= 12)].set_index('Date')['ID expérience'].resample('M').count()

    # Afficher les résultats
    print(avis_par_mois_2022)

    #Combien d'avis ont été posté en 2023 ? 
    avis_2023 = filtered_data[filtered_data['Date'].dt.year == 2023].groupby('Date')['ID expérience'].value_counts()

    avis_2023 = avis_2023.sum()

    print(avis_2023)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(label="Nombre d'avis émis en 2019", value=avis_2019)
    col2.metric(label="Nombre d'avis émis en 2020", value=avis_2020)
    
    col3.metric(label="Nombre d'avis émis en 2021", value=avis_2021)
    col4.metric(label="Nombre d'avis émis en 2022", value=avis_2022)
    col1, col2= st.columns(2)

    with col1:

        chart_height = 400  # Hauteur en pixels
        chart_width = 600  # Largeur en pixels

        # Afficher le graphique avec la taille spécifiée
        fig = px.pie(filtered_data, names='Ressenti usager', height=chart_height, width=chart_width)
        fig.update_traces(textinfo='percent+value')
        
        # Afficher le graphique avec Streamlit
        st.subheader("Ressenti des utilisateurs")

        st.plotly_chart(fig)
    with col2:
        # Tracer le graphique en utilisant une pie chart avec Plotly Express
        chart_height = 400  # Hauteur en pixels
        chart_width = 600  # Largeur en pixels

        # Afficher le graphique avec la taille spécifiée
        fig = px.pie(filtered_data, names='Etat expérience', height=chart_height, width=chart_width)

        # Afficher le graphique avec Streamlit
        st.subheader("Répartition des demandes traitées et non traitées")
        st.plotly_chart(fig)
    
   
    count_by_month = filtered_data['Mois'].value_counts().sort_index()
    chart_data = pd.DataFrame({'Mois': count_by_month.index.strftime('%Y-%m'), 'Nombre d\'avis': count_by_month.values})
    
    st.subheader("Evolution du nombre total d'avis")

    st.line_chart(chart_data.set_index('Mois'))


    # Compter le nombre de valeurs A, B et C par mois
    count_by_month_value = filtered_data.groupby(['Mois', 'Ressenti usager']).size().unstack().fillna(0)
    count_by_month_value.index = count_by_month_value.index.strftime('%Y-%m')

    # Tracer le graphique avec st.line_chart()
    st.subheader("Evolution du nombre d'avis selon le ressenti des usagers")

    st.line_chart(count_by_month_value)

    count_by_region = filtered_data['Intitulé région usager'].value_counts().sort_index()
    
    st.subheader("Nombre d'avis par région")

    st.bar_chart(count_by_region)

    count_by_region_value = filtered_data.groupby(['Intitulé région usager', 'Ressenti usager']).size().unstack().fillna(0)
    
    st.subheader("Nombre d'avis selon le ressenti des usagers")

    st.bar_chart(count_by_region_value)
   

    geolocator = Nominatim(user_agent="my_app")

    # Créer une carte Folium centrée sur la France
    map_france = folium.Map(location=[46.603354, 1.888334], zoom_start=6, tiles = "Stamen Toner")

    departements = filtered_data['Intitulé département usager'].unique()

    for departement in departements:
        departement_str = str(departement)  # Convertir en chaîne de caractères
        location = geolocator.geocode(departement_str + ", France")
        if location:
            latitude = location.latitude
            longitude = location.longitude
            # Ajouter un marqueur sur la carte pour chaque département
            folium.Marker([latitude, longitude], popup=departement_str).add_to(map_france)

    # Afficher la carte
    map_france






elif selected_tab == "pole emploi":

    # Garder uniquement les lignes contenant plusieurs valeurs spécifiques
    df2 = df
    valeurs_specifiques = [None, 'AGENCE POLE EMPLOI (APE)', 'POLE EMPLOI']
    mask = df2['Intitulé Typologie 1'].isin(valeurs_specifiques)
    df2 = df2[mask]

    # Réinitialiser les index des lignes
    df2 = df2.reset_index(drop=True)

    # Afficher le dataframe résultant
    st.write(df2)


    import plotly.express as px
    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(df2, names="Ressenti usager")
        fig.update_traces(textinfo='percent+value')

        # Afficher le graphique avec Streamlit
        st.plotly_chart(fig)
    with col2:
        # Tracer le graphique en utilisant une pie chart avec Plotly Express
        fig = px.pie(df2, names='Etat expérience')

        # Afficher le graphique avec Streamlit
        st.plotly_chart(fig)


    df2[['Date', 'Heure']] = df2['Date de publication'].str.split('T', expand=True)
    df2['Date'] = pd.to_datetime(df2['Date'])
    df2['Mois'] = df2['Date'].dt.to_period('M')
    count_by_month = df2['Mois'].value_counts().sort_index()
    chart_data = pd.DataFrame({'Mois': count_by_month.index.strftime('%Y-%m'), 'Nombre d\'avis': count_by_month.values})
    st.line_chart(chart_data.set_index('Mois'))


    # Compter le nombre de valeurs A, B et C par mois
    count_by_month_value = df2.groupby(['Mois', 'Ressenti usager']).size().unstack().fillna(0)
    count_by_month_value.index = count_by_month_value.index.strftime('%Y-%m')

    # Tracer le graphique avec st.line_chart()
    st.line_chart(count_by_month_value)


    count_by_region = df2['Intitulé région usager'].value_counts().sort_index()

    st.bar_chart(count_by_region)

    count_by_region_value = df2.groupby(['Intitulé région usager', 'Ressenti usager']).size().unstack().fillna(0)
    st.bar_chart(count_by_region_value)


