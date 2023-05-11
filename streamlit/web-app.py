"""
# My first app
Here's our first attempt at using data to create a table:
"""
import pandas as pd
import streamlit as st
import numpy as np


st.set_page_config(page_title="Service-publics", page_icon=":books:", layout="wide")

header = "<div style='display: flex; align-items: center;'><h1>Services publics </h1><img src='https://emojipedia-us.s3.amazonaws.com/source/skype/289/squid_1f991.png' alt='Image de calamar' style='width:40px;height:40px;'></div>"

st.markdown(header, unsafe_allow_html=True)

st.subheader('Ce qui ce dit sur les réseaux')

data = pd.read_csv('export-structures.csv', sep=';')

st.write(data)
counts = data['Intitulé du réseau'].value_counts()

# chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=["a", "b", "c"])

# st.bar_chart(chart_data)

# Afficher le graphique dans Streamlit
# Créer un DataFrame avec les données pour le graphique
chart_data = pd.DataFrame({'Intitulé du réseau': counts.index, 'Occurrences': counts.values}).sort_values('Occurrences', ascending=False)

# Afficher le graphique à barres dans Streamlit
st.bar_chart(chart_data.set_index('Intitulé du réseau'))
