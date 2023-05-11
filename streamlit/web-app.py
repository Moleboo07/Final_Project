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
dash = <iframe src="https://opendata.plus.transformation.gouv.fr/explore/embed/dataset/export-experiences/analyze/?dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6ImV4cG9ydC1leHBlcmllbmNlcyIsIm9wdGlvbnMiOnt9fSwiY2hhcnRzIjpbeyJhbGlnbk1vbnRoIjp0cnVlLCJ0eXBlIjoibGluZSIsImZ1bmMiOiJDT1VOVCIsInlBeGlzIjoiaWRfZXhwZXJpZW5jZSIsInNjaWVudGlmaWNEaXNwbGF5Ijp0cnVlLCJjb2xvciI6InJhbmdlLUFjY2VudCJ9XSwieEF4aXMiOiJkYXRlX2FjdGlvbl9lbmdhZ2VlIiwibWF4cG9pbnRzIjoiIiwidGltZXNjYWxlIjoieWVhciIsInNvcnQiOiIiLCJzZXJpZXNCcmVha2Rvd24iOiJldmFsdWF0aW9uX3V0aWxlX3JlcG9uc2Vfc3RydWN0dXJlXzFfcGFyX3Zpc2l0ZXVycyJ9XSwiZGlzcGxheUxlZ2VuZCI6dHJ1ZSwiYWxpZ25Nb250aCI6dHJ1ZX0%3D&static=false&datasetcard=false" width="400" height="300" frameborder="0"></iframe>
st.write(dash)
