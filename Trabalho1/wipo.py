import re, json

filename = "WIPOPearl_COVID-19_Glossary.xml"

with open(filename, 'r', encoding='utf-8') as file:
    ficheiro = file.read()

#Remocao de linhas não necessárias
ficheiro = re.sub(r"</?page.*?>",r"",ficheiro) #serve para remover a tag page 

padrao = r'<text.*font="(1|15|22)".*>.*</text>\n?'
padrao2 = r'<text.*top="(65|1131|1158|1185)".*>.*</text>\n?' #Remove texto dos cabeçalhos e rodape (nº paginas ...)
ficheiro = re.sub(padrao, r"", ficheiro)
ficheiro = re.sub(padrao2, r"", ficheiro)
ficheiro = re.sub(r'<text.*font="8".*><b>(.*)</b></text>\n?',r"*\1 *\n",ficheiro) #poe o nome do termo entre *
ficheiro = re.sub(r'<text.*font="11".*>(.*)</text>\n?', r"@\1\n", ficheiro) #poe a categoria a começar com @
ficheiro = re.sub (r"</?text.*?>", "", ficheiro) 
ficheiro = re.sub (r"- ", "", ficheiro) #usado para tirar quando é quebra de linha 
ficheiro = re.sub('^\s*$', r"", ficheiro, flags=re.MULTILINE) #Remove linhas vazias
ficheiro = re.sub (r"<i>", "", ficheiro) 
ficheiro = re.sub (r"</i>", "", ficheiro)

# Ajuste para unir linhas de fonte "8" (nome do termo) consecutivas
ficheiro = re.sub(r'\*\n\*(.*?)\*\n', r'\1*\n', ficheiro)

padrao3 = r'\*(.*?)\s+\*\n(.*?)\n@(.*?)\n((?:(?!\*|@).)*)'
correspondencias = re.findall(padrao3, ficheiro, re.DOTALL)


glossario = {}
for correspondencia in correspondencias:
    termo = correspondencia[0].strip()
    descricao = correspondencia[1].strip()
    categoria = correspondencia[2].strip()
    traducoes_raw = correspondencia[3].strip()
    traducoes = re.split(r'<b>\s*(.*?)\s*</b>', traducoes_raw)[1:] #divide quando encontra uma nova lingua
    
    #limpeza antes de meter no documento
    termo = re.sub (r"\*", "", termo)
    termo = re.sub (r"\n", " ", termo)
    descricao = re.sub (r"<b>", "", descricao)
    descricao = re.sub (r"</b>", "", descricao)
    descricao = re.sub (r"\n", "", descricao)
    traducoes = [re.sub(r"\n", "", traducao) for traducao in traducoes]
    
    glossario[termo] = {
        "Descricao": descricao,
        "Categoria": categoria,
        "Traducoes": {traducoes[i].strip(): traducoes[i+1].strip() for i in range(0, len(traducoes), 2)}
    }
    
file_out = open("wipo.json","w",encoding= 'utf-8')
json.dump(glossario,file_out,indent=4,ensure_ascii=False)
file_out.close()
    

