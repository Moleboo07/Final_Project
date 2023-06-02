import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.preprocessing import MultiLabelBinarizer

df = pd.read_csv("C:\\Users\\poire\\OneDrive\\Bureau\\topic_pe\\channel.csv", sep=";")
# Chargement des données à partir du DataFrame
print(df.shape)
comments = df['Description'].tolist()
channels = df['Canaux Typologie 1'].tolist()
#print(df['Canaux Typologie 1'].unique())
#print(channels)


#liste des mots possibles
mots_possibles = ['demarche en ligne', 'compte ou espace personnel', 'telephone', 'e-mail', 'courrier', 'accueil', 'reseaux sociaux']

#fonction pour vérifier si un enregistrement contient au moins un des mots des canaux
def check_canaux(row):
    canaux = row['Canaux Typologie 1']
    if isinstance(canaux, list):
        return any(mot in canaux for mot in mots_possibles)
    return canaux in mots_possibles

#filtrer les enregistrements qui contiennent au moins un des mots des canaux
df_filtre = df[df.apply(check_canaux, axis=1)]

print(df_filtre.shape)
#fonction pour vérifier la présence d'un mot dans ma liste
def check_mot(mot, liste):
    if mot in liste:
        return 1
    return 0

#création des colonnes binaires pour chaque mot possible
for mot in mots_possibles:
    df_filtre[mot] = df_filtre['Canaux Typologie 1'].apply(lambda x: check_mot(mot, x))

print(df_filtre['Canaux Typologie 1'][3])
print(df_filtre['demarche en ligne'])

df_APE_DL = df_filtre[df_filtre['demarche en ligne'] == 1]
df_APE_DL = df_APE_DL.loc[:, ['Description', 'demarche en ligne']]
new_df_2 = df_filtre.loc[:, ['Description', 'demarche en ligne', 'compte ou espace personnel', 'telephone', 'e-mail', 'courrier', 'accueil', 'reseaux sociaux']]

df_APE_DL.to_csv('C:\\Users\\poire\\OneDrive\\Bureau\\topic_pe\\APE_DL.csv', encoding='utf-8', sep=';', index=False)
new_df_2.to_csv('C:\\Users\\poire\\OneDrive\\Bureau\\topic_pe\\channel_complet_2.csv', encoding='utf-8', sep=';', index=False)
#df_APE_DL.to_csv('C:\\Users\\poire\\OneDrive\\Bureau\\topic_pe\\APE_DL.csv', encoding='utf-8', sep=';', index=False)



mlb = MultiLabelBinarizer()
y = mlb.fit_transform(channels)
print(y)

y = mlb.fit_transform([label.split(",") for label in channels])
print(y)