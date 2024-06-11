import json
import re
import torch
from transformers import AutoTokenizer, AutoModel

json1 = 'C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/conceitos.json'
json2 = 'C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/termos_glossario.json'
json3 = 'C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/termos_anatomia.json'
json4 = 'C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/wipo_modificado.json'
json5 = 'C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/doencas_site.json'

with open(json1, 'r', encoding='utf-8') as file:
    conceitos = json.load(file)

with open(json2, 'r', encoding='utf-8') as file:
    termos = json.load(file)
    
with open(json3, 'r', encoding='utf-8') as file:
    anatomia = json.load(file)
    
with open(json4, 'r', encoding='utf-8') as file:
    traducoes = json.load(file)

with open(json5, 'r', encoding='utf-8') as file:
    doencas = json.load(file)

glossario = conceitos

# Carrega o modelo e o tokenizer do BioBERT
model_name = "dmis-lab/biobert-base-cased-v1.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Função para calcular a similaridade entre duas palavras usando BioBERT
def calcular_similaridade(frase1, frase2, tokenizer, model):
    inputs1 = tokenizer(frase1, return_tensors='pt')
    inputs2 = tokenizer(frase2, return_tensors='pt')

    with torch.no_grad(): #Desativa o cálculo de gradientes pois é feita apenas inferência e economiza memória e torna o processo mais rápido
        outputs1 = model(**inputs1) #Passa os tokens da primeira frase pelo modelo para obter as saídas
        outputs2 = model(**inputs2)

    embeddings1 = outputs1.last_hidden_state.mean(dim=1) #Calcula a média das representações da última camada oculta para todos os tokens da primeira frase
    embeddings2 = outputs2.last_hidden_state.mean(dim=1)

    cos = torch.nn.CosineSimilarity(dim=1) #Define a função de similaridade coseno.
    similaridade = cos(embeddings1, embeddings2).item() #Retorna a similaridade calculada entre as duas frases

    return similaridade


for termo, informacao in termos.items():
    if termo.lower() in conceitos:
        # Se o termo já existir em conceitos.json, adicione uma nova chave "Descricao 2" com a nova informação
        glossario[termo]["Descricao 2"] = informacao
    else:
        # Se o termo não existir em conceitos.json, adicione-o ao dicionário conceitos com todas as suas informações
        glossario[termo] = {"Categoria": "Sem Categoria","Descricao": informacao,}

for termo, informacao in anatomia.items():
    if termo.lower() in conceitos:
        # Se o termo já existir em conceitos.json, adicione uma nova chave "Descricao Anatomia" com a nova informação
        glossario[termo]["Descricao Anatomica"] = informacao
    else:
        # Se o termo não existir em conceitos.json, adicione-o ao dicionário conceitos com todas as suas informações
        glossario[termo] = {"Categoria": "Sem Categoria","Descricao": informacao,}
        
for termo, informacao in doencas.items():
    if termo in conceitos:
        # Se o termo já existir em conceitos.json, adicione uma nova chave "Descricao SNS" com a nova informação
        glossario[termo]["Descricao SNS"] = informacao
    else:
        # Se o termo não existir em conceitos.json, adicione-o ao dicionário conceitos com todas as suas informações
        glossario[termo] = {"Categoria": "Sem Categoria","Descricao": informacao,}


# Junta de acordo com a tradução em portugues no wipo. Verifica se a tradução é igual ao nome dos conceitos ou se são de termos parecidos (95% de semelhança)
for termo, informacao in traducoes.items():
    traducao_pt = informacao["Traducoes"]["PT"].lower()
    traducao_total = informacao["Traducoes"]
    
    # Verificar se a tradução PT está nos conceitos
    if traducao_pt in conceitos:
        glossario[traducao_pt] = conceitos[traducao_pt]
        glossario[traducao_pt]["Traducoes"] = traducao_total
    else:
        
        # Verificar similaridade com as chaves em conceitos
        for conceito, dados_conceito in conceitos.items():
            conceito_lower = conceito.lower()
            
            if (len(conceito_lower.split()) == 1) and (len(traducao_pt.split()) == 1): # compara conceitos cujo nome só tenha 1 palavra
                similaridade = calcular_similaridade(traducao_pt, conceito_lower, tokenizer, model)
                
                if similaridade > 0.95: # acima de 95% de similariedade
                    glossario[conceito_lower] = dados_conceito
                    glossario[conceito_lower]["Traducoes Relacionadas"] = traducao_total
        else:
            pass

    
file_out = open("C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/glossario_geral.json","w",encoding= 'utf-8')
json.dump(glossario,file_out,indent=4,ensure_ascii=False)
file_out.close()