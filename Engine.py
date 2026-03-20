import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException,Timeout
from bs4 import BeautifulSoup
import random
import re
import pandas as pd
from datetime import datetime
import os
import numpy as np
import matplotlib.pyplot as plt

class Engine:
    def __init__(self):
        self.url = ""
        self.html = False

    def Request(self, url: str) -> bool:
        """Télécharge la page et retourne True si succès, False sinon."""
        self.url = url
        self.html = False # On réinitialise à False pour chaque nouvelle requête
        
        headers_list = [
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Cache-Control": "max-age=0"
            }
            ]
        try:
            headers = random.choice(headers_list)
            self.html = False
            # A list of user agent because if there is only one agent, it will blocked
            
            reponse = requests.get(url=url,headers=headers,timeout=3)

            """ Management of many Error """

            reponse.raise_for_status()

            self.html = reponse.text
            return True
        
        except ConnectionError as erreur:
            print(f'Connection error: {erreur}')
        except HTTPError as erreur:
            print(f'HTTP Error: {erreur.response.status_code}')
        except RequestException as erreur:
            print(f'Requests exception error: {erreur}')
        except Timeout as erreur:
            print(f'Timeout over: {erreur}')
    
    def Return_price_Amazon(self):
        if self.html: # verification wheares url existing

            self.regexAmazon =r"/(dp|gp/product)/([A-Z0-9]{10})"
            match_amazon = re.search(self.regexAmazon,self.url)
            
            if bool(match_amazon):
                soup = BeautifulSoup(self.html,'html.parser')

                try: # Capture of price
                    balise_prix = soup.find("span", class_="a-price")
                    if not balise_prix:
                        print("The price is not found")
                        return
                    prix_brut = balise_prix.find("span", class_="a-offscreen").text
                    prix = prix_brut.replace("$", "").replace(",", ".").replace('€',"")
                    prix_clean = float(prix)
                    self.prix = prix_clean

                    """ Exportation """
                    fichier_existe = os.path.isfile(self.nom_fichier)

                    donnée = {
                        "product":[self.name],
                        "date":[datetime.now().strftime("%Y-%m-%d %H:%M")],
                        "price":[prix_clean]
                        }
                    
                    df = pd.DataFrame(donnée)

                    df.to_csv(
                    self.nom_fichier, 
                    mode='a',              
                    index=False,       
                    header=not fichier_existe,
                    sep=';'
                    )



                    print(f'Price: {prix_clean} | Price saved')
                except AttributeError:
                    print(f'Error of scrapting')
            else:
                print(f"Url {self.url} is not recognised like an url recognised.")
        else:
            print('You have not page to analyse')
        
    def Name_product(self,name):
        name = str(name).lower().strip()
        self.name = name
        self.nom_fichier =  str(self.name) + ".csv"
        print('Name saved')
    
    def Analise_products_price(self):
        if self.name:
            df_produit = pd.read_csv(self.nom_fichier,sep=';',on_bad_lines='skip')

            date = pd.to_datetime(df_produit['date'])
            prix = df_produit['price']

            plt.figure(figsize=(10, 5))
            plt.plot(date,prix,marker='o',color='b', label=f'Price of {self.name}')
            plt.title("Evolution of price")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.legend()

            plt.xticks(rotation=45)

            plt.savefig(f'{self.name}.png')

            



g = Engine()
g.Name_product('iphone')
g.Request('https://www.amazon.fr/gp/product/B0C3YMHJ3R/ref=ox_sc_act_title_1?smid=A1X6FK5RDHNB96&th=1')
g.Return_price_Amazon()
g.Analise_products_price()