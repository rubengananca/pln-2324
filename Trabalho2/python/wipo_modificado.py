import json
import re

with open('C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/wipo.json', 'r', encoding='utf-8') as file:
    dados = json.load(file)

# Expressão regular para remover tudo depois de ", (syn.)" para depois fazer a comparação do portugues traduzido com os outros json 
padrao = r', \(syn\.\).*'

# Função recursiva para percorrer o JSON e aplicar a regex
def aplicar_regex(dados): #percorre o JSON de forma recursiva
    if isinstance(dados, dict): #isinstance é usado para verificar o tipo de dados 
        for key, value in dados.items():
            if isinstance(value, dict): #Se encontrar um dicionário, itera sobre seus itens
                aplicar_regex(value)
            elif isinstance(value, str): #se encontrar uma string, aplica a regex
                dados[key] = re.sub(padrao, '', value)
    elif isinstance(dados, list): #se encontrar uma lista, itera sobre os elementos da lista
        for i in range(len(dados)):
            dados[i] = aplicar_regex(dados[i])
    return dados

dados = aplicar_regex(dados)

# Se quiser salvar as modificações de volta ao arquivo JSON
with open('C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/wipo_modificado.json', 'w', encoding='utf-8') as file:
    json.dump(dados, file, ensure_ascii=False, indent=4)