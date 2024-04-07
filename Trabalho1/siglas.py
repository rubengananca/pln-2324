import re, json

filename = "siglas.xml"

with open(filename, 'r', encoding='utf-8') as file:
    ficheiro = file.read()

#Remocao de linhas não necessárias
ficheiro = re.sub(r"</?page.*?>",r"",ficheiro) 
ficheiro = re.sub(r"</?image.*?>",r"",ficheiro) 

padrao = r'<text.*font="(22|15|25|23|11)".*>.*</text>\n?' #padrao para remover tudo o que for texto com font="15" ou "22" ...
padrao2 = r'<text.*top="238".*>.*</text>\n?' #Remove texto dos cabeçalhos 
ficheiro = re.sub(padrao, r"", ficheiro)
ficheiro = re.sub(padrao2, r"", ficheiro)
ficheiro = re.sub (r"</?text.*?>", "", ficheiro) #*? para ele parar no primeiro > e não retirar info importante
ficheiro = re.sub (r"- ", "", ficheiro) 
ficheiro = re.sub (r"–", "", ficheiro)  #era usado para separar o nome da sigla da sua descricao
ficheiro = re.sub('^\s*$', r"", ficheiro, flags=re.MULTILINE) #Remove linhas vazias

siglas = re.findall(r"<b>(.+?)</b>\n([^<]+)",ficheiro) #separa a sigla da sua descricao

# Processar as siglas
novos_conceitos = [] 
for designacao,descricao in siglas:
    nova_desig = designacao.strip()
    nova_desig = re.sub (r"\n", "", nova_desig)
    nova_descri = descricao.strip()    
    nova_descri = re.sub (r"\n", "", nova_descri)
    novos_conceitos.append((nova_desig,nova_descri))


conceitos_dict = dict(novos_conceitos)

file_out = open("siglas.json","w",encoding= 'utf-8')
json.dump(conceitos_dict,file_out,indent=4,ensure_ascii=False)
file_out.close()

