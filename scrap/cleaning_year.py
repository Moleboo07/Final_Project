import pandas as pd

from datetime import datetime, timedelta


data = pd.read_csv("scrap_final.csv",sep=",", encoding="utf-8")
data

def convert_word_number(col):
  if "semaine" in col['rel_date']:
      if "il y a une semaine" in col['rel_date']:
        new_val = col['rel_date'].replace("il y a une semaine", "il y a 1 mois")
      else:
          new_val = col['rel_date']
  elif "jour" in col['rel_date']:
      new_val = col['rel_date'].replace("un","1")
  elif "mois" in col['rel_date']:
      new_val = col['rel_date'].replace("un","1")
  elif "an" in col['rel_date']:
      new_val = col['rel_date'].replace("un","1")

  else:
      new_val = col['rel_date']
  
  return new_val

data['convert_1'] = data.apply(convert_word_number, axis=1)



# Obtenez la date actuelle
date_actuelle = datetime(2023, 5, 1) 


def extraire_annee(row):
    if 'mois' in row['convert_1']:
        mois = int(row['convert_1'].split()[3])
        annee = (date_actuelle - timedelta(days=30 * mois)).year

    elif 'semaines'in row['convert_1']:
        annee = (date_actuelle).year

    elif 'jour'in row['convert_1']:
        annee = (date_actuelle).year

    elif 'jours'in row['convert_1']:
        annee = (date_actuelle).year

    elif 'heures'in row['convert_1']:
        annee = (date_actuelle).year

    elif 'an' in row['convert_1']:
        ans = int(row['convert_1'].split()[3])
        annee = date_actuelle.year - ans
    else:
        annee = None
    return annee



data['annee'] = data.apply(extraire_annee, axis=1)


data = data.drop(index=data[data['annee'] < 2021 ].index)
data= data.reset_index(drop=True)


import csv
data.to_csv('year_cleaning.csv', quoting=csv.QUOTE_ALL, sep=';',index=False)

print(data)

