from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time

import pandas as pd

review_texts = []
ratings = []
rel_dates = []


# configuration des options de Chrome
options = Options()
options.add_argument("--lang=en")

# initialisation du webdriver
driver = webdriver.Chrome(options=options)

# navigation vers une page Web
url = "https://www.google.com/maps/place/P%C3%B4le+emploi/@44.0911466,6.2435074,17z/data=!4m6!3m5!1s0x12cb854cd9a53289:0x5a8967b2cf01a2f4!8m2!3d44.091215!4d6.243275!16s%2Fg%2F1tpfg31_/"
driver.get(url)

# cliquer sur le bouton "Trier" et sélectionner l'option "Plus récent"
# wait = WebDriverWait(driver, 50)
skip = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[1]/div/div/button/span')
skip.click()

time.sleep(8)
avis = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]/div[2]/div[2]')
avis.click()

time.sleep(5)
filtre = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[8]/div[2]/button/span')
filtre.click()

time.sleep(3)
recent = driver.find_element(By.XPATH, '//*[@id="action-menu"]/div[2]')
recent.click()

time.sleep(5)


try:
    more_btns = driver.find_elements(By.XPATH, '//*[@class="w8nwRe kyuRq"]')
        
except NoSuchElementException:
    more_btns = None


if more_btns:
    for m in more_btns:
        m.click()
        print("button clicked")  
        # print(m)        
        time.sleep(4)


# parcourir les avis et extraire les différentes informations
        
while True:
    response = BeautifulSoup(driver.page_source, 'html.parser')
    rlist = response.find_all('div', class_='GHT2ce')
    # print("\n la liste rlist : ",len(rlist))
    # print("\n ************************************************************ \n")
    
    new_list = []
    
    for i in range(1,len(rlist),2):
        new_list.append(rlist[i])
        
    # print("\n la liste new : ",len(new_list))
    # print("\n ************************************************************ \n")
    
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
            rating_span = r.find('div', class_='DU9Pgb').find('span', class_='kvMYJc')
            rating = rating_span['aria-label']
            ratings.append(rating)
            print(rating)
            print("\n")
        except Exception:
            aucun = "Aucun"
            ratings.append(aucun)
            # ratings.append(None)
            rating = None
                    
        try:
            rel_date = r.find('div', class_='DU9Pgb').find('span', class_='rsqaWe').text
            rel_dates.append(rel_date)
            print(rel_date)
            print("\n")
        except Exception:
            aucun = "Aucun"
            rel_dates.append(aucun)
            # rel_dates.append(None)
            rel_date = None

        print ("****************************************************** \n")

    # fermeture du navigateur
    driver.quit()

    # Création du dataframe
    df = pd.DataFrame({
        'review_text': review_texts,
        'rating': ratings,
        'rel_date': rel_dates
    })

    df.to_csv("scrap_1.csv", index=False)

    print(df)