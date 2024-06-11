# Transformação do documento Glossário de Termos Médicos Técnicos e Populares.pdf para formato xml

# Análise inicial do documento xml e remoção manual de algumas informações

# Removeram-se as primeiras duas linhas do documento xml manualmente

import re
import json

filename = "C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/xml/GlossaÌ_rio de Termos MeÌ_dicos TeÌ_cnicos e Populares.xml"
with open(filename,'r', encoding= 'utf-8') as f:
    texto = f.read()




# data cleaning
    
texto = re.sub(r"</?page.*>", "", texto)  # remoção dos pages
texto = re.sub(r"</?text.*?>", "", texto)  # remoção da tag texto e todo o conteúdo dentro da mesma, nomeadamente posição na página e fonte
texto = re.sub(r"</?fontspec.*?>", "", texto) # remoção da linha com a informação fontspec
texto = re.sub (r"<i>", "",texto) # remoção da tag itálico, onde se encontra a descrição de cada termo
texto = re.sub (r"</i>", "",texto) # remoção da parte final da tag 
texto = re.sub(r"<b>[A-Z]</b>", "", texto) # remoção das linhas onde Aparece a ordem alfabética das palavras
texto = texto.lower()

# --------------- documento após o tratamento inicial de data cleaning -------------------- #

resultado=open("C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/texts/glossario_inicial.txt", "w", encoding='UTF-8')
resultado.write(texto)
resultado.close()

# -------------- criação de lista com todas as designações presentes no doc ---------------- #

lista_designacoes = re.findall(r"<b>(.*)</b>", texto) 


texto2 = re.sub(r"<b>(.*)</b>", "", texto)  # remoção das designações do documento porque já foram guardadas em lista

texto2 = re.sub(r"\(pop\)", "@@", texto2)    # alteração da expressão pop para o marcador @
texto2 = re.sub(r"@@  @@", "@@" , texto2)

texto2= re.sub(r"\n+", "", texto2)
texto2 = re.sub(r"\s,", "", texto2)         # resolução dos casos indesejados em que os símbolos apareciam seguidos e separados por espaço
texto2 = texto2.lower()

# ---------------- guardar documento com as descrições ------------------------ #

result=open("C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/texts/glossario.txt", "w", encoding='UTF-8')
result.write(texto2)
result.close()

# em glossário .txt o nº de @ é 3647 o que está direito



lista2 = re.findall(r"@(?:\s|,|X)(.*?)@", texto2)
lista3= re.findall(r"(^.*?)\s@", texto2) # devido à regex em cima utilizada, a primeira descrição não é captada uma vez que não é antecedida por nenhum @.
lista_descricoes = lista3 + lista2

print(len(lista2))

#for x in lista_descricoes:
#    print("NOVO", x)

print(len(lista_designacoes))
print(len(lista_descricoes))

termos = [[x, y] for x, y in zip(lista_designacoes, lista_descricoes)]

dicionario={}
dicionario = dict(termos)


out = open ("C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/termos_glossario.json", "w", encoding="utf-8")
json.dump(dicionario, out, ensure_ascii=False, indent=4)
out.close()



