from bs4 import BeautifulSoup
import requests
import json
import time
import re

# link da página do sns
url_base = "https://www.chlo.min-saude.pt/index.php/component/seoglossary/1-glossario?start="


# User-Agent é um cabeçalho HTTP que os navegadores e outras aplicações enviam em cada requisição. Ele identifica o cliente (navegador, crawler, etc.) para o servidor.
# É necessário senão algumas requisições não funcionam

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

#Função pra extrair do site os conceitos e a descrição dos conceitos 
def extrai_doencas(url):
    result = requests.get(url, headers=headers)
    if result.status_code != 200:
        print(f"Failed to retrieve page: {url} with status code {result.status_code}")
        return {}
    
    html = result.text
    soup = BeautifulSoup(html, "html.parser")
    
    rows = soup.find_all("tr", class_=["row0", "row1"])
    
    dicionario_doencas = {}

    for row in rows:
        a_tag = row.find("a")
        p_tag = row.find("p")
        
        if a_tag and p_tag:
            desig = a_tag.text.strip()
            desig = desig.lower()
            desig = re.sub(r' ', ' ', desig) #Remover um caracter estranho
            descri = p_tag.get_text(strip=True)
            descri = descri.lower()
            descri = re.sub(r' ', ' ', descri)
            
            dicionario_doencas[desig] = descri

    if not dicionario_doencas:
        print(f"No diseases found on page: {url}")
        
    return dicionario_doencas

#itera sobre cada página e retira a info
def extrai_doencas_paginas(url_base, num_paginas):
    res = {}
    
    for i in range(num_paginas):
        url = f"{url_base}{i * 15}"  
        print(f"Processing page: {url}") #Ajuda a fazer debug
        dicti = extrai_doencas(url)
        res.update(dicti)
        time.sleep(2)  # Adicionar um pequeno atraso entre as solicitações
    
    return res


num_paginas = 26  # número de páginas a percorrer
res = extrai_doencas_paginas(url_base, num_paginas)

# Ordena e escreve no arquivo JSON
sorted_dict = dict(sorted(res.items()))

with open("C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/doencas_site.json", "w", encoding="utf-8") as f_out:
    json.dump(sorted_dict, f_out, indent=4, ensure_ascii=False)

print(f"Total diseases extracted: {len(sorted_dict)}")
