import requests
from bs4 import BeautifulSoup
import random


class Engine:
    def Request(self,url:str):

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
        
        reponse = requests.get(url=url,headers={"User-Agent": random.choice(user_agents)})

        if reponse.status_code != 200:
            raise ConnectionError
        self.html = reponse.text
    
    def Return_price_Amazon(self):
        soup = BeautifulSoup(self.html,'html.parser')

        balises = soup.find(class_='a-spacing-top-mini apex-core-price-identifier')
        prix = balises.find(class_='a-offscreen').text
        prix = prix.replace("$", "").replace(",", ".").replace('€',"")
        prix_clean = float(prix)

        print(prix_clean)


g = Engine()
g.Request('https://www.amazon.fr/Nintendo-Inazuma-Eleven-Strikers/dp/B008DSOIOU/ref=sr_1_1?dib=eyJ2IjoiMSJ9.BZXhkQM6SUKpRS3ty_VMIjXpDuU6ra6t4xnepXMRh88PHXdzDPd1ANevZYxuxnwFgyLSLLpUcqaY7uMenq5p9is-If_ecsKvvcOYYWiDW5jkcZOJbX3z2uFE23zMnSPBAH1VigXIfu5FsDjhSDFNsaUZ20tbrd9qSulpw6JbVv1C9iAe2O8DiR74Ezm688siTxzBpuJttu-fULUG7BIWzbdLYNixDBtqjP4erlsAUvHS4r9ySAIF_ccWSRzK1vRd2_t_OzDsZYgkvR4WqRR7bacyVBnrMYyg2EBo72f62ik.-WWqaq0o-0FBCmy_2EUIhLMjWy3zlA0uW5Qiip36osk&dib_tag=se&keywords=inazuma+eleven+switch&qid=1774015112&sr=8-1')
g.Return_price_Amazon()
        