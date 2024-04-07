import json

json1 = 'conceitos.json'
json2 = 'termos_glossario.json'
json3 = 'termos_anatomia.json'

with open(json1, 'r', encoding='utf-8') as file:
    conceitos = json.load(file)

with open(json2, 'r', encoding='utf-8') as file:
    termos = json.load(file)
    
with open(json3, 'r', encoding='utf-8') as file:
    anatomia = json.load(file)

glossario = conceitos
        
for termo, informacao in termos.items():
    if termo in conceitos:
        # Se o termo já existir em conceitos.json, adicione uma nova chave "Descricao 2" com a nova informação
        glossario[termo]["Descricao 2"] = informacao
    else:
        # Se o termo não existir em conceitos.json, adicione-o ao dicionário conceitos com todas as suas informações
        glossario[termo] = {"Categoria": "Sem Categoria","Descricao": informacao,}

for termo, informacao in anatomia.items():
    if termo in conceitos:
        # Se o termo já existir em conceitos.json, adicione uma nova chave "Descricao Anatomia" com a nova informação
        glossario[termo]["Descricao Anatomica"] = informacao
    else:
        # Se o termo não existir em conceitos.json, adicione-o ao dicionário conceitos com todas as suas informações
        glossario[termo] = {"Categoria": "Sem Categoria","Descricao": informacao,}
    
file_out = open("glossario_geral.json","w",encoding= 'utf-8')
json.dump(glossario,file_out,indent=4,ensure_ascii=False)
file_out.close()