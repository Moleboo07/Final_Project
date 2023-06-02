"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import plotly.express as px
# import folium
# from geopy.geocoders import Nominatim
# from streamlit_folium import folium_static
# from PIL import Image



st.set_page_config(page_title="Service-publics", page_icon=":books:", layout="wide")
# logo = Image.open('final/logo.png')

# st.image(logo, width=100)
st.title("Services publics")

# Charger les données depuis le fichier CSV
df = pd.read_csv("export-experiences.csv", sep=";")
df2 = pd.read_csv("year_cleaning_1.csv", sep=";")

#import csv SP
df_sp_glo = pd.read_csv("final/topic_glo_sp.csv", sep=";")
df_sp_tel = pd.read_csv("final/topic_tel_sp.csv", sep=";")
df_sp_mail = pd.read_csv("final/topic_mail_sp.csv", sep=";")
df_sp_info = pd.read_csv("final/topic_info_sp.csv", sep=";")
df_sp_accueil = pd.read_csv("final/topic_accueil_sp.csv", sep=";")

#import csv PN
df_pn_glo = pd.read_csv("final/topic_glo_scrap.csv", sep=";")
df_pn_tel = pd.read_csv("final/topic_tel_scrap.csv", sep=";")
df_pn_mail = pd.read_csv("final/topic_mail_scrap.csv", sep=";")
df_pn_info = pd.read_csv("final/topic_info_scrap.csv", sep=";")
df_pn_accueil = pd.read_csv("final/topic_accueil_scrap.csv", sep=";")

#import csv global
df_glo = pd.read_csv("final/topic_glo.csv", sep=";")
df_glo_tel = pd.read_csv("final/topic_tel(1).csv", sep=";")
df_glo_mail = pd.read_csv("final/topic_mail.csv", sep=";")
df_glo_info = pd.read_csv("final/topic_info.csv", sep=";")
df_glo_accueil = pd.read_csv("final/topic_info.csv", sep=";")

option_1 = st.selectbox(
'Sélectionnez :',
('Analyse SP+', 'Analyse PN+', 'Analyse globale'))

st.write('Vous avez sélectionné :', option_1)

if option_1 == 'Analyse SP+':

    # geolocator = Nominatim(user_agent="my_app")

    #     # Créer une carte Folium centrée sur la France
    # map_france = folium.Map(location=[46.603354, 1.888334], zoom_start=6, tiles="Stamen Toner")

    # departements = df['Intitulé département usager'].unique()

    # for departement in departements:
    #     departement_str = str(departement)  # Convertir en chaîne de caractères
    #     location = geolocator.geocode(departement_str + ", France")
    #     if location:
    #         latitude = location.latitude
    #         longitude = location.longitude
    #             # Ajouter un marqueur sur la carte pour chaque département
    #         folium.Marker([latitude, longitude], popup=departement_str).add_to(map_france)

    #     # Afficher la carte

    # folium_static(map_france)
    df[['Date', 'Heure']] = df['Date de publication'].str.split('T',n=1, expand=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Mois'] = df['Date'].dt.to_period('M')


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
    for option, column in option_mapping.items():
        if len(eval(option)) > 0:
            query = query[query[column].isin(eval(option))]
    filtered_data = query
 

    #Combien d'avis ont été posté en 2021 ? 
    avis_2021 = filtered_data[filtered_data['Date'].dt.year == 2021].groupby('Date')['ID expérience'].value_counts()
    avis_2021 = avis_2021.sum()
    avis_par_mois_2021 = filtered_data[filtered_data['Date'].dt.year == 2021].set_index('Date')['ID expérience'].resample('M').count()

    #Combien d'avis ont été posté en 2022 ? 
    avis_2022 = filtered_data[filtered_data['Date'].dt.year == 2022].groupby('Date')['ID expérience'].value_counts()
    avis_2022 = avis_2022.sum()
    avis_par_mois_2022 = filtered_data[(filtered_data['Date'].dt.year == 2022) & (filtered_data['Date'].dt.month >= 1) & (filtered_data['Date'].dt.month <= 12)].set_index('Date')['ID expérience'].resample('M').count()

    #Combien d'avis ont été posté en 2023 ? 
    avis_2023 = filtered_data[filtered_data['Date'].dt.year == 2023].groupby('Date')['ID expérience'].value_counts()
    avis_2023 = avis_2023.sum()


    col1, col2, col3 = st.columns(3)

    col1.metric(label="Nombre d'avis émis en 2021", value=avis_2021)
    col2.metric(label="Nombre d'avis émis en 2022", value=avis_2022)
    col3.metric(label="Nombre d'avis en 2023", value=avis_2023)

    col1, col2= st.columns(2)

    with col1:
        #Pie Chart ressenti utilisateur 
        chart_height = 400  
        chart_width = 600  
        fig = px.pie(filtered_data, names='Ressenti usager', height=chart_height, width=chart_width)
        fig.update_traces(textinfo='percent+value')
        st.subheader("Ressenti des utilisateurs")
        st.plotly_chart(fig)

    with col2:
        #¨Pie Chart demandes traitées et non traitées 
        chart_height = 400  
        chart_width = 600  
        fig = px.pie(filtered_data, names='Etat expérience', height=chart_height, width=chart_width)
        st.subheader("Répartition des demandes traitées et non traitées")
        st.plotly_chart(fig)

    #Graphique d'évolution du nb d'avis 
    count_by_month = filtered_data['Mois'].value_counts().sort_index()
    chart_data = pd.DataFrame({'Mois': count_by_month.index.strftime('%Y-%m'), 'Nombre d\'avis': count_by_month.values})
    st.subheader("Evolution du nombre total d'avis")
    st.line_chart(chart_data.set_index('Mois'))

    # Graphique d'évolution du nb d'avis par région
    count_by_month_value = filtered_data.groupby(['Mois', 'Ressenti usager']).size().unstack().fillna(0)
    count_by_month_value.index = count_by_month_value.index.strftime('%Y-%m')

    st.subheader("Evolution du nombre d'avis selon le ressenti des usagers")
    st.line_chart(count_by_month_value)

    count_by_region = filtered_data['Intitulé région usager'].value_counts().sort_index()
    st.subheader("Nombre d'avis par région")
    st.bar_chart(count_by_region)

    count_by_region_value = filtered_data.groupby(['Intitulé région usager', 'Ressenti usager']).size().unstack().fillna(0)
    st.subheader("Nombre d'avis selon le ressenti des usagers")
    st.bar_chart(count_by_region_value)


    #Menu Déroulant choix du médium 
    st.subheader("Choix du médium :")

    option_2 = st.selectbox(
    'Sélectionnez :',
    ('Email', 'Téléphone', 'Démarche en ligne', 'Accueil', 'Global'))

    st.write('Vous avez sélectionné :', option_2)

    if option_2 == 'Email' :
        st.write(df_sp_mail)
        df_filtered = df_sp_mail[df_sp_mail['clusters'] != -1]
        count_by_topic = df_filtered['clusters'].value_counts().sort_index()
        #count_by_topic = df_sp_mail['clusters'].value_counts().sort_index()
        st.subheader("Nombre de commentaires par topic")
        st.bar_chart(count_by_topic)
    elif option_2 == 'Téléphone' :
        st.write(df_sp_tel)
        df_filtered = df_sp_tel[df_sp_tel['clusters'] != -1]
        count_by_topic = df_filtered['clusters'].value_counts().sort_index()
        #count_by_topic = df_sp_tel['clusters'].value_counts().sort_index()
        st.subheader("Nombre de commentaires par topic")
        st.bar_chart(count_by_topic)

    elif option_2 == 'Démarche en ligne' :
        st.write(df_sp_info)
        df_filtered = df_sp_info[df_sp_info['clusters'] != -1]
        count_by_topic = df_filtered['clusters'].value_counts().sort_index()
        #count_by_topic = df_sp_info['clusters'].value_counts().sort_index()
        st.subheader("Nombre de commentaires par topic")
        st.bar_chart(count_by_topic)

    elif option_2 == 'Accueil' :
        st.write(df_sp_accueil)
        df_filtered = df_sp_accueil[df_sp_accueil['clusters'] != -1]
        count_by_topic = df_filtered['clusters'].value_counts().sort_index()
        #count_by_topic = df_sp_accueil['clusters'].value_counts().sort_index()
        st.subheader("Nombre de commentaires par topic")
        st.bar_chart(count_by_topic)

    elif option_2 == 'Global' :
        st.write(df_sp_glo)
        df_filtered = df_sp_glo[df_sp_glo['clusters'] != -1]
        count_by_topic = df_filtered['clusters'].value_counts().sort_index()
        #count_by_topic = df_sp_glo['clusters'].value_counts().sort_index()
        st.subheader("Nombre de commentaires par topic")
        st.bar_chart(count_by_topic)


elif option_1 == "Analyse PN+" : 
    pole_emplois = df2['entite'].unique()
    pole_emploi = st.multiselect('Pôle emploi', pole_emplois, key="pole_emploi_multiselect")

    option_mapping = {
            # 'concours_1': 'concours',
        
            'pole_emploi' : 'entite',
        }

    query = df2
    for option, column in option_mapping.items():
        if len(eval(option)) > 0:
            query = query[query[column].isin(eval(option))]
    df2 = query

    # #Nb de commentaires par PE 
    comm_pe = df2['entite'].value_counts()
    comm_pe = comm_pe.sum()

    # Calculer la moyenne des notes par ville
    moyenne_notes = df2.groupby('entite')['rating'].mean()
    moyenne_notes=moyenne_notes.mean()

    col1, col2= st.columns(2)
    col1.metric(label="Nombre de commentaires", value= comm_pe)
    col2.metric(label="Note moyenne", value=moyenne_notes)

    # Evolution du nb de commentaires par années 
    comm_pe_annee_2021 = df2[df2['annee'] == 2021]['entite'].value_counts()
    comm_pe_annee_2021 = comm_pe_annee_2021.sum()
    comm_pe_annee_2022 = df2[df2['annee'] == 2022]['entite'].value_counts()
    comm_pe_annee_2022 = comm_pe_annee_2022.sum()
    comm_pe_annee_2023 = df2[df2['annee'] == 2023]['entite'].value_counts()
    comm_pe_annee_2023 = comm_pe_annee_2023.sum()

    col1, col2, col3= st.columns(3)
    col1.metric(label="Commentaires émis en 2021", value=comm_pe_annee_2021)
    col2.metric(label="Commentaires émis en 2022", value=comm_pe_annee_2022)
    col3.metric(label="Commentaires émis en 2023", value=comm_pe_annee_2023)

    option = st.selectbox(
    'Sélectionnez :',
    ('Analyse SP+', 'Analyse PN+', 'Démarche en ligne', 'Accueil'))

    #Menu Déroulant choix du médium 
    st.subheader("Choix du médium :")

    option_3 = st.selectbox(
    'Sélectionnez :',
    ('Email', 'Téléphone', 'Démarche en ligne', 'Accueil', 'Global'))

    st.write('Vous avez sélectionné :', option_3)

    if option_3 == 'Email' :
        st.write(df_pn_mail)
        df_filtered = df_pn_mail[df_pn_mail['clusters'] != -1]
        count_by_topic = df_filtered['clusters'].value_counts().sort_index()
        #count_by_topic = df_pn_mail['clusters'].value_counts().sort_index()
        st.subheader("Nombre de commentaires par topic")
        st.bar_chart(count_by_topic)
 
    elif option_3 == 'Téléphone' :
        st.write(df_pn_tel)
        df_filtered = df_pn_tel[df_pn_tel['clusters'] != -1]
        count_by_topic = df_filtered['clusters'].value_counts().sort_index()
        #count_by_topic = df_pn_tel['clusters'].value_counts().sort_index()
        st.subheader("Nombre de commentaires par topic")
        st.bar_chart(count_by_topic)

    elif option_3 == 'Démarche en ligne' :
        st.write(df_pn_info)
        df_filtered = df_pn_info[df_pn_info['clusters'] != -1]
        count_by_topic = df_filtered['clusters'].value_counts().sort_index()
        #count_by_topic = df_pn_info['clusters'].value_counts().sort_index()
        st.subheader("Nombre de commentaires par topic")
        st.bar_chart(count_by_topic)

    elif option_3 == 'Accueil' :
        st.write(df_pn_accueil)
        df_filtered = df_pn_accueil[df_pn_accueil['clusters'] != -1]
        count_by_topic = df_filtered['clusters'].value_counts().sort_index()
        #count_by_topic = df_pn_accueil['clusters'].value_counts().sort_index()
        st.subheader("Nombre de commentaires par topic")
        st.bar_chart(count_by_topic)

    elif option_3 == 'Global' :
        st.write(df_pn_glo)
        df_filtered = df_pn_glo[df_pn_glo['clusters'] != -1]
        count_by_topic = df_filtered['clusters'].value_counts().sort_index()
        #count_by_topic = df_pn_glo['clusters'].value_counts().sort_index()
        st.subheader("Nombre de commentaires par topic")
        st.bar_chart(count_by_topic)

elif option_1 == 'Analyse globale' : 
    #Menu Déroulant choix du médium 
    st.subheader("Choix du médium :")

    option_4 = st.selectbox(
    'Sélectionnez :',
    ('Email', 'Téléphone', 'Démarche en ligne', 'Accueil', 'Global'))

    st.write('Vous avez sélectionné :', option_4)

    if option_4 == 'Email' :
        st.write(df_glo_mail)
        df_filtered = df_glo_mail[df_glo_mail['clusters'] != -1]
        count_by_topic = df_filtered['clusters'].value_counts().sort_index()
        #count_by_topic = df_glo_mail['clusters'].value_counts().sort_index()
        st.subheader("Nombre de commentaires par topic")
        st.bar_chart(count_by_topic)

    elif option_4 == 'Téléphone' :
        st.write(df_glo_tel)
        df_filtered = df_glo_tel[df_glo_tel['clusters'] != -1]
        count_by_topic = df_filtered['clusters'].value_counts().sort_index()
        #count_by_topic = df_glo_tel['clusters'].value_counts().sort_index()
        st.subheader("Nombre de commentaires par topic")
        st.bar_chart(count_by_topic)

    elif option_4 == 'Démarche en ligne' :
        st.write(df_glo_info)
        df_filtered = df_glo_info[df_glo_info['clusters'] != -1]
        count_by_topic = df_filtered['clusters'].value_counts().sort_index()
        #count_by_topic = df_glo_info['clusters'].value_counts().sort_index()
        st.subheader("Nombre de commentaires par topic")
        st.bar_chart(count_by_topic)


    elif option_4 == 'Accueil' :
        st.write(df_glo_accueil)
        df_filtered = df_glo_accueil[df_glo_accueil['clusters'] != -1]
        count_by_topic = df_filtered['clusters'].value_counts().sort_index()
        #count_by_topic = df_glo_accueil['clusters'].value_counts().sort_index()
        #count_by_topic_filtered = count_by_topic[count_by_topic != -1]

        st.subheader("Nombre de commentaires par topic")
        st.bar_chart(count_by_topic)


    elif option_4 == 'Global' :
        st.write(df_glo)
        df_filtered = df_glo[df_glo['clusters'] != -1]
        count_by_topic = df_filtered['clusters'].value_counts().sort_index()
        #count_by_topic = df_glo['clusters'].value_counts().sort_index()
        st.subheader("Nombre de commentaires par topic")
        st.bar_chart(count_by_topic)


    

# Garder uniquement les lignes contenant plusieurs valeurs spécifiques
# valeurs_specifiques = [None, 'AGENCE POLE EMPLOI (APE)', 'POLE EMPLOI']
# mask = df2['Intitulé Typologie 1'].isin(valeurs_specifiques)
# df2 = df2[mask]

# # Réinitialiser les index des lignes
# df2 = df2.reset_index(drop=True)

# # Afficher le dataframe résultant
# st.write(df2)


#import plotly.express as px
#col1, col2 = st.columns(2)

# with col1:

#     fig = px.pie(df2, names="Ressenti usager")
#     fig.update_traces(textinfo='percent+value')

#     # Afficher le graphique avec Streamlit
#     st.plotly_chart(fig)
# with col2:
#     # Tracer le graphique en utilisant une pie chart avec Plotly Express
#     fig = px.pie(df2, names='Etat expérience')

#     # Afficher le graphique avec Streamlit
#     st.plotly_chart(fig)


# df2[['Date', 'Heure']] = df2['Date de publication'].str.split('T', expand=True)
# df2['Date'] = pd.to_datetime(df2['Date'])
# df2['Mois'] = df2['Date'].dt.to_period('M')
# count_by_month = df2['Mois'].value_counts().sort_index()
# chart_data = pd.DataFrame({'Mois': count_by_month.index.strftime('%Y-%m'), 'Nombre d\'avis': count_by_month.values})
# st.line_chart(chart_data.set_index('Mois'))


# Compter le nombre de valeurs A, B et C par mois
# count_by_month_value = df2.groupby(['Mois', 'Ressenti usager']).size().unstack().fillna(0)
# count_by_month_value.index = count_by_month_value.index.strftime('%Y-%m')

# # Tracer le graphique avec st.line_chart()
# st.line_chart(count_by_month_value)


# count_by_region = df2['Intitulé région usager'].value_counts().sort_index()

# st.bar_chart(count_by_region)

# count_by_region_value = df2.groupby(['Intitulé région usager', 'Ressenti usager']).size().unstack().fillna(0)
# st.bar_chart(count_by_region_value)
