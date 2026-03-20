import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException,Timeout
from bs4 import BeautifulSoup
import random


class Engine:
    def Request(self,url:str):
        try:
            self.html = False
            user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",

        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) "
        "Gecko/20100101 Firefox/123.0",

        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",

        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/17.0 Safari/605.1.15",

        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
        "Mobile/15E148 Safari/604.1",

        "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        ]
            
            reponse = requests.get(url=url,headers={"User-Agent": random.choice(user_agents)},timeout=3)

            reponse.raise_for_status()

            self.html = reponse.text
        
        except ConnectionError as erreur:
            print(f'Connection error: {erreur}')
        except HTTPError as erreur:
            print(f'HTTP Error: {erreur}')
        except RequestException as erreur:
            print(f'Requests exception error: {erreur}')
        except Timeout as erreur:
            print(f'Timeout over: {erreur}')
    
    def Return_price_Amazon(self):
        if self.html:
            soup = BeautifulSoup(self.html,'html.parser')

            balises = soup.find(class_='a-spacing-top-mini apex-core-price-identifier')
            prix = balises.find(class_='a-offscreen').text
            prix = prix.replace("$", "").replace(",", ".").replace('€',"")
            prix_clean = float(prix)

            print(prix_clean)


g = Engine()
g.Request('https://www.amazon.fr/GRIFEMA-GA1201-12-trotinette-electrique-Portails/dp/B0C3YMHJ3R/?_encoding=UTF8&pd_rd_w=BIT1C&content-id=amzn1.sym.f1302343-9817-4aee-a01c-cc93646e7acc&pf_rd_p=f1302343-9817-4aee-a01c-cc93646e7acc&pf_rd_r=5T9D7JS9F7CNPPSHM7EY&pd_rd_wg=u5XEO&pd_rd_r=21f4643f-619f-4cef-94b7-68e0d98af88e&ref_=pd_hp_d_btf_crs_zg_bs_325614031&th=1')
g.Return_price_Amazon()
        