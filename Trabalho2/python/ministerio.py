import re, json

filename = "C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/xml/glossario_ministerio_saude.xml"

with open(filename, 'r', encoding='utf-8') as file:
    ficheiro = file.read()

#Remocao de linhas não necessárias
ficheiro = re.sub(r"</?page.*?>",r"",ficheiro) #serve para remover a tag page 
ficheiro = re.sub(r"</?pdf2xml.*?>",r"",ficheiro)
ficheiro = re.sub(r"</?image.*?>",r"",ficheiro) 

padrao = r'<text.*font="(22|15|25|23)".*>.*</text>\n?' #padrao para remover tudo o que for texto com font="15" ou "22" ...
padrao2 = r'<text.*top="238".*>.*</text>\n?' #Remove texto dos cabeçalhos 
ficheiro = re.sub(padrao, r"", ficheiro)
ficheiro = re.sub(padrao2, r"", ficheiro)
ficheiro = re.sub (r"</?text.*?>", "", ficheiro) #*? para ele parar no primeiro > e não retirar info importante
ficheiro = re.sub (r"<i>Categoria: </i>", "*", ficheiro)
ficheiro = re.sub (r"- ", "", ficheiro) #usado para tirar quando é quebra de linha
ficheiro = re.sub (r" – ", "-", ficheiro)  
ficheiro = re.sub('^\s*$', r"", ficheiro, flags=re.MULTILINE) #Remove linhas vazias
ficheiro = re.sub (r"<i>", "", ficheiro) #É preciso ser retirado isto porque há termos em ingles em italico como "Western blot"
ficheiro = re.sub (r"</i>", "", ficheiro)

ficheiro = re.sub(r'</b>\n<b>(.*?)</b>\n', r'\1</b>\n', ficheiro) #Junta duas linhas consecutivas de <b> ou seja de nome de termos cortados

lista = re.findall(r"<b>(.*?)</b>\n(?:\*\n)?(.*?)\n(.*?)<b>", ficheiro, re.DOTALL)

# Processar os termos
novos_conceitos = [] 
glossario = {}
for termo, categoria, descricao in lista:
    novo_termo = termo.strip()
    novo_termo = re.sub (r"<b>", "", novo_termo) 
    novo_termo = re.sub (r"</b>", "", novo_termo)
    novo_termo = re.sub (r"\n", "", novo_termo)
    novo_termo = novo_termo.lower()
    nova_categoria = categoria.strip() 
    nova_categoria = re.sub (r"<b>", "", nova_categoria) 
    nova_categoria = re.sub (r"</b>", "", nova_categoria)
    nova_categoria = re.sub (r"\n", "", nova_categoria)
    nova_categoria = nova_categoria.lower()
    nova_descricao = descricao.strip()
    nova_descricao = re.sub (r"\n", "", nova_descricao)
    nova_descricao = nova_descricao.lower()
    if novo_termo not in glossario:
        if nova_descricao !="":
            glossario[novo_termo] = {"Categoria": nova_categoria, "Descricao": nova_descricao}
        elif nova_descricao == "": #Quando não tem categoria um termo - antes a descrição era atribuida a categoria então foi necessário trocar
            glossario[novo_termo] = {"Categoria": "Sem Categoria", "Descricao": nova_categoria}

file_out = open("C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/conceitos.json","w",encoding= 'utf-8')
json.dump(glossario,file_out,indent=4,ensure_ascii=False)
file_out.close()

