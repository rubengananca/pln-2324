import json
import re

file = "C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/glossario_geral.json"
with open(file, 'r', encoding='utf-8') as file:
    doencas = json.load(file)

# Criar um novo dicionário para armazenar as chaves modificadas
doencas_modificadas = {}

# Remover pontos finais das chaves e armazenar no novo dicionário
for doenca, info in doencas.items():    
    nova_doenca = re.sub(r"\.$", "", doenca)  # Remove o ponto final no final da chave
    doencas_modificadas[nova_doenca] = info  # Armazena a nova chave no novo dicionário

# Ordenar o dicionário modificado por chaves em ordem alfabética
doencas_ordenadas = dict(sorted(doencas_modificadas.items()))

# Escrever o JSON ordenado para o arquivo de saída
file_out = open("C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/glossario_geral.json", "w", encoding='utf-8')
json.dump(doencas_ordenadas, file_out, indent=4, ensure_ascii=False)
file_out.close()
