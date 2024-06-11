# Transformação do documento anatomia geral.pdf para formato xml

# Análise inicial do documento xml e remoção manual de algumas informações

# Removeram-se as primeiras linhas do documento xml manualmente

import re
import json

filename = "C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/xml/anatomia geral.xml"
with open(filename,'r', encoding= 'utf-8') as f:
    texto = f.read()


# data cleaning
    
texto = re.sub(r"</?page.*>", "", texto)  # remoção dos pages
texto = re.sub(r"</pdf2xml>","", texto)
texto = re.sub(r"</?fontspec.*?>", "", texto)  # remoção da linha com a informação fontspec
texto = re.sub(r"<text[^>]*\s*>\s*[A-Z]((, [A-Z])+)?<\/text>", "", texto) # remoção de linhas contendo apenas letras maiúsculas que consistem em legenda das imagens
texto = re.sub(r"<text[^>]*>\s*(\d+)\s*</text>", "", texto) # remoção de linhas com digitos correspondentes a legenda da imagem
texto = re.sub(r'<image[^>]*>', '', texto) # remoção das imagens
texto = re.sub(r'<text.*font="(1|4|8|9|10|11|12|14|15|16|17|18|19)".*>.*</text>\n',"",texto) # remoção de informação não relevante, através da fonta utilizada
texto = re.sub(r'\n{2,}', '\n', texto)
texto = re.sub(r'^\s+|\s+$', '', texto, flags=re.MULTILINE)
texto= re.sub(r'<text[^>]*\sfont="3"[^>]*>\s*(.*?)\s*</text>', r'\1', texto)


# Marcação das designações com os caracteres @@

texto = re.sub(r'<text[^>]*\sfont="([567])"[^>]*>(.*?)</text>', r'@@\2', texto) 
texto = re.sub(r'(<text[^>]*\sfont="13"[^>]*>)(.*?)(</text>)', r'@@\2', texto)
texto = re.sub(r'@@<([bi])>(.*?)</\1>', r'@@\2', texto) # remoção das tags bold e italic após a marcação



# --------------- documento após data cleaning e marcação -------------------- #

resultado=open("C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/texts/glossario_anatomia_inicial.txt", "w", encoding='UTF-8')
resultado.write(texto)
resultado.close()

# Capturar designações e descrições
matches = re.findall(r'@@\s*(.+?)(?=\n@@|$)', texto, re.DOTALL)

# Criar dicionário com designações e descrições
dicionario = {}
for match in matches:
    linhas = match.strip().split('\n')
    designacao = linhas[0]
    designacao = designacao.lower()
    descricao = '\n'.join(linhas[1:]) if len(linhas) > 1 else "Sem Descrição"
    descricao = descricao.replace('\n', '')
    descricao = re.sub(r"\s[A-Z]((, [A-Z])+)?$", "",descricao)
    descricao = descricao.lower()
    dicionario[designacao] = descricao


out = open ("C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/termos_anatomia.json", "w", encoding="utf-8")
json.dump(dicionario, out, ensure_ascii=False, indent=4)
out.close()