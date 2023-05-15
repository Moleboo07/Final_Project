from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time

import pandas as pd



# configuration des options de Chrome
options = Options()
options.add_argument("--lang=en")

# Initialisation du webdriver
driver = webdriver.Chrome(options=options)


url = "https://www.google.com/maps/@44.091215,6.243275,17z"
driver.get(url)

# Cliquer sur le bouton "Refuser les cookies"
skip = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[1]/div/div/button/span')
skip.click()
time.sleep(5)



data = pd.read_csv("pole_emploi_struc_test.csv", sep=";", encoding="ISO-8859-1")

data.info()
entities = data['Libelle'].tolist()

# print(entity)
while True:
    for entity in entities:
        print(entity)


        review_texts = []
        ratings = []
        rel_dates = []


        # Saisie de l'antenne de pôle emploi 
        saisie = driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
        saisie.clear()
        saisie.send_keys(entity, Keys.ENTER)
        # saisie
        time.sleep(3)


        # Acceder à l'onglet "Avis"
        avis = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]/div[2]/div[2]')
        avis.click()
        time.sleep(4)

        # Cliquer sur le bouton "Trier"
        filtre = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[8]/div[2]/button/span')
        filtre.click()
        time.sleep(3)


        # Sélectionner l'option "Plus récent"
        recent = driver.find_element(By.XPATH, '//*[@id="action-menu"]/div[2]')
        recent.click()
        time.sleep(4)


        x = len(driver.find_elements(By.XPATH, '//*[@class="jJc9Ad "]'))
        print("************************************************** \n")
        print(x)
        print("************************************************** \n")


        # Appuyer de la touche "End" pour pouvoir scroller la page
        while True:
            driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]').send_keys(Keys.END)
            time.sleep(3)
            new_nb = len(driver.find_elements(By.XPATH, '//*[@class="jJc9Ad "]'))
            if new_nb == x:
                break
            x = new_nb
            print("################################################## \n")
            print(x)
            print("\n")



        # Appuyer sur le bouton "plus" pour charger la totalité de messages dans les cas où on ne les a pas 
        try:
            more_btns = driver.find_elements(By.XPATH, '//*[@class="w8nwRe kyuRq"]')
                
        except NoSuchElementException:
            more_btns = None

        if more_btns:
            for m in more_btns:
                m.click()
                print("button clicked")  
                time.sleep(3)
                
                
                

        # Parcourir les avis et extraire les différentes informations
                
        while True:
            response = BeautifulSoup(driver.page_source, 'html.parser')
            rlist = response.find_all('div', class_='GHT2ce')

            new_list = []
            
            for i in range(1,len(rlist),2):
                new_list.append(rlist[i])
            
            for r in new_list:
                
                try:
                    review_div = r.find('div', class_='MyEned')
                    review_text = None
                    if review_div:
                        review_text = review_div.find('span', class_='wiI7pd').text
                        review_texts.append(review_text)
                        print(review_text)
                        print("\n")
                    else:
                        aucun = "Aucun"
                        review_texts.append(aucun)
                        print("Pas de commentaire")
                except Exception as e:
                    print(e)
                    review_text = None
                            
                
                try:
            
                    star = r.find_all('img', {'class': 'hCCjke vzX5Ic'})
                    rating = len(star)
                    ratings.append(rating)
                    print(rating)
                    print("\n")
                except Exception:
                    aucun = "Aucun"
                    ratings.append(aucun)
                    rating = None            
                    
                            
                try:
                    rel_date = r.find('div', class_='DU9Pgb').find('span', class_='rsqaWe').text
                    rel_dates.append(rel_date)
                    print(rel_date)
                    print("\n")
                except Exception:
                    aucun = "Aucun"
                    rel_dates.append(aucun)
                    rel_date = None

                print ("****************************************************** \n")

            break
    # Création du dataframe
    df = pd.DataFrame({
        'review_text': review_texts,
        'rating': ratings,
        'rel_date': rel_dates
    })

    # df.to_csv("scrap_1.csv", index=False)

    print(df)  
            
        # Fermeture du navigateur
    driver.quit()
            
            