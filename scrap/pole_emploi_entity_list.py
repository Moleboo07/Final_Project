import pandas as pd
# import numpy as np


data = pd.read_csv("pole_emploi_struc_test.csv", sep=";", encoding="ISO-8859-1")


# data = data.drop(['Intitulé du réseau','IntitulÃ© de la typologie','IntitulÃ© de la structure','Description de la structure','Code postal de la structure','Ville','Pays'], axis=1)
# data_1 = data.dropna()

data.info()
entity = data['Libelle'].tolist()

print(entity)

for i in entity:
    print(i)