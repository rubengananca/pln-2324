import shutil
from flask import Flask, render_template, request, redirect, url_for
import json
import os
from collections import defaultdict

app = Flask(__name__)

file = "C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/glossario_geral.json"
with open(file, 'r', encoding='utf-8') as file:
    doencas = json.load(file)
    
def guardar_conceitos(doencas, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(doencas, file, ensure_ascii=False, indent=4)
        
def carregar_conceitos(file):
    with open(file, 'r', encoding='utf-8') as file:
        doencas = json.load(file)
    return doencas

@app.route("/")
def home():
    tamanho = len(doencas)
    return render_template("home.html", tamanho = tamanho)

@app.route("/doencas")
def listar_doencas():
    #Sempre que entra na página carrega o ficheiro para estar atualizado
    doencas = carregar_conceitos("C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/glossario_geral.json")
    # Agrupar as doenças por letra
    doencas_por_letra = defaultdict(list)
    for doenca in doencas:
        primeira_letra = doenca[0].upper()

        # Junta as letras com acento à letra normal
        if primeira_letra == "Á":
            doencas_por_letra["A"].append(doenca)
        elif primeira_letra == "Â":
            doencas_por_letra["A"].append(doenca)
        elif primeira_letra == "É":
            doencas_por_letra["E"].append(doenca)
        elif primeira_letra == "Í":
            doencas_por_letra["I"].append(doenca)
        elif primeira_letra == "Ó":
            doencas_por_letra["O"].append(doenca)
        elif primeira_letra == "Ú":
            doencas_por_letra["U"].append(doenca)
        else:
            doencas_por_letra[primeira_letra].append(doenca)
    return render_template("doencas.html", doencas_por_letra=doencas_por_letra) 

def obter_categorias(caminho):
    doencas = carregar_conceitos(caminho)
    lista_categorias = []
    for conceito, info in doencas.items():
        categoria = info["Categoria"]
        categoria = categoria.capitalize()  # torna apenas a primeira letra em maiúscula
        if categoria not in lista_categorias:
            lista_categorias.append(categoria)
    return sorted(lista_categorias)

@app.route("/categorias")
def listar_categorias():
    caminho_json = "C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/glossario_geral.json"
    lista_ordenada = obter_categorias(caminho_json)
    return render_template("categorias.html", lista_ordenada=lista_ordenada)


@app.route("/categorias/<categoria>")
def consultar_categoria(categoria):
    # Carrega o json para tar atualizado
    doencas = carregar_conceitos("C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/glossario_geral.json")
    
    # Filtra os conceitos pela categoria
    conceitos_filtrados = {conceito: detalhes for conceito, detalhes in doencas.items() if detalhes['Categoria'].upper() == categoria.upper()}
    
    return render_template("consultar_categoria.html", categoria=categoria, conceitos=conceitos_filtrados)

@app.route("/doenca/<designacao>") 
def consultar_doencas(designacao):
    desig = doencas[designacao]
    categoria = desig["Categoria"]
    descricao = desig["Descricao"]
    
    descricao_2 = desig.get("Descricao 2")  # O get permite que não dê erro caso a chave não exista
    descricao_sns = desig.get("Descricao SNS")
    descricao_utilizador = desig.get("Descricao Utilizador")
    traducoes = desig.get("Traducoes", {})
    traducoes_rel = desig.get("Traducoes Relacionadas", {})


    traducoes_ar = traducoes.get("AR")
    traducoes_de = traducoes.get("DE")
    traducoes_es = traducoes.get("ES")
    traducoes_fr = traducoes.get("FR")
    traducoes_ja = traducoes.get("JA")
    traducoes_ko = traducoes.get("KO")
    traducoes_pt = traducoes.get("PT")
    traducoes_ru = traducoes.get("RU")
    traducoes_zh = traducoes.get("ZH")
    
    traducoes_rel_ar = traducoes_rel.get("AR")
    traducoes_rel_de = traducoes_rel.get("DE")
    traducoes_rel_es = traducoes_rel.get("ES")
    traducoes_rel_fr = traducoes_rel.get("FR")
    traducoes_rel_ja = traducoes_rel.get("JA")
    traducoes_rel_ko = traducoes_rel.get("KO")
    traducoes_rel_pt = traducoes_rel.get("PT")
    traducoes_rel_ru = traducoes_rel.get("RU")
    traducoes_rel_zh = traducoes_rel.get("ZH")
    
    return render_template("descricao.html",categoria = categoria, descricao = descricao, descricao_2 = descricao_2, descricao_sns = descricao_sns, descricao_utilizador = descricao_utilizador,
                           traducoes_ar=traducoes_ar,traducoes_de=traducoes_de,traducoes_es=traducoes_es,traducoes_fr=traducoes_fr, traducoes_ja=traducoes_ja,
                           traducoes_ko =traducoes_ko, traducoes_pt = traducoes_pt, traducoes_ru = traducoes_ru, traducoes_zh = traducoes_zh,
                           traducoes=traducoes, traducoes_rel = traducoes_rel,
                           traducoes_rel_ar=traducoes_rel_ar,traducoes_rel_de=traducoes_rel_de,traducoes_rel_es=traducoes_rel_es,traducoes_rel_fr=traducoes_rel_fr, traducoes_rel_ja=traducoes_rel_ja,
                           traducoes_rel_ko =traducoes_rel_ko, traducoes_rel_pt = traducoes_rel_pt, traducoes_rel_ru = traducoes_rel_ru, traducoes_rel_zh = traducoes_rel_zh,                           
                           designacao = designacao)  
  
@app.route("/doenca/<designacao>/editar", methods=["GET", "POST"])
def editar_conceitos(designacao):
    global doencas,filename
    
    if request.method == "GET": # É importante existir para quando a página é aberta pela primeira vez aparecerem os dados expostos
        desig = doencas[designacao]
        categoria = desig["Categoria"]
        descricao = desig["Descricao"]
        descricao_2 = desig.get("Descricao 2")
        descricao_sns = desig.get("Descricao SNS")
        descricao_utilizador = desig.get("Descricao Utilizador")
        traducoes = desig.get("Traducoes", {})
        traducoes_rel = desig.get("Traducoes Relacionadas", {})
        
        traducoes_ar = traducoes.get("AR")
        traducoes_de = traducoes.get("DE")
        traducoes_es = traducoes.get("ES")
        traducoes_fr = traducoes.get("FR")
        traducoes_ja = traducoes.get("JA")
        traducoes_ko = traducoes.get("KO")
        traducoes_pt = traducoes.get("PT")
        traducoes_ru = traducoes.get("RU")
        traducoes_zh = traducoes.get("ZH")
        
        traducoes_rel_ar = traducoes_rel.get("AR")
        traducoes_rel_de = traducoes_rel.get("DE")
        traducoes_rel_es = traducoes_rel.get("ES")
        traducoes_rel_fr = traducoes_rel.get("FR")
        traducoes_rel_ja = traducoes_rel.get("JA")
        traducoes_rel_ko = traducoes_rel.get("KO")
        traducoes_rel_pt = traducoes_rel.get("PT")
        traducoes_rel_ru = traducoes_rel.get("RU")
        traducoes_rel_zh = traducoes_rel.get("ZH")
        
        lista_categorias = obter_categorias("C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/glossario_geral.json")
        
        return render_template("editar.html",categoria = categoria, descricao = descricao, descricao_2 = descricao_2, descricao_sns = descricao_sns, descricao_utilizador = descricao_utilizador,
                           traducoes=traducoes, traducoes_rel = traducoes_rel,    
                           traducoes_ar=traducoes_ar,traducoes_de=traducoes_de,traducoes_es=traducoes_es,traducoes_fr=traducoes_fr, traducoes_ja=traducoes_ja,
                           traducoes_ko =traducoes_ko, traducoes_pt = traducoes_pt, traducoes_ru = traducoes_ru, traducoes_zh = traducoes_zh,
                           traducoes_rel_ar=traducoes_rel_ar,traducoes_rel_de=traducoes_rel_de,traducoes_rel_es=traducoes_rel_es,traducoes_rel_fr=traducoes_rel_fr, traducoes_rel_ja=traducoes_rel_ja,
                           traducoes_rel_ko =traducoes_rel_ko, traducoes_rel_pt = traducoes_rel_pt, traducoes_rel_ru = traducoes_rel_ru, traducoes_rel_zh = traducoes_rel_zh,                           
                           designacao = designacao, lista_categorias=lista_categorias)  
        
    elif request.method == "POST": # Para alterar os dados
        categoria = request.form["categoria"]
        descricao_utilizador = request.form["descricao_utilizador"]
        nova_lingua = request.form["nova_lingua"]
        lingua_descricao = request.form["lingua_descricao"]
        
        if nova_lingua!="vazio" and lingua_descricao!="": #Para acrescentar uma lingua que não exista ou atualizar
            if "Traducoes" not in doencas[designacao] and "Traducoes Relacionadas" not in doencas[designacao]:  # Não existe nenhuma tradução, adiciona de raiz
                doencas[designacao]["Traducoes"] = {nova_lingua: lingua_descricao}
            elif "Traducoes" in doencas[designacao]: # Existem traducoes entao muda a chave relacionada com elas
                doencas[designacao]["Traducoes"][nova_lingua] = lingua_descricao
            elif "Traducoes Relacionadas" in doencas[designacao]: # Existem traducoes relacionadas entao muda a chave relacionada com elas. Se não houvesse diferenciação dava erro ou não estaria a ser atribuido corretamente
                doencas[designacao]["Traducoes Relacionadas"][nova_lingua] = lingua_descricao
            
        if categoria!="vazio":
            doencas[designacao]["Categoria"] = categoria
        
        if descricao_utilizador:
            doencas[designacao]["Descricao Utilizador"] = descricao_utilizador

        guardar_conceitos(doencas,"C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/glossario_geral.json")
        
        if "glossario_backup.json" in os.listdir("C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json"): #guarda também no backup se ele existir, o backup está sempre atualizado
            guardar_conceitos(doencas, "C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/glossario_backup.json")
        
        return redirect(url_for("consultar_doencas", designacao=designacao))

@app.route("/doenca/<designacao>/eliminar", methods=["POST"])
def eliminar_conceito(designacao):
    caminho_json = "C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/glossario_geral.json"
    doencas = carregar_conceitos(caminho_json)
    
    # Verifica se o conceito com a designação fornecida existe
    if designacao in doencas:
        # Realiza um backup do arquivo antes de fazer alterações
        shutil.copyfile(caminho_json, "C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/glossario_backup.json")

        del doencas[designacao]

        # Guarda as alterações no arquivo JSON
        guardar_conceitos(doencas, caminho_json)

        # Redireciona para a página de listagem de doenças após a eliminação
        return redirect(url_for("listar_doencas"))

    # Caso o conceito não exista, retorna uma mensagem de erro
    return "O conceito não existe."

# Faz a tabela e usa js
@app.route("/tabela")
def table():
    doencas = carregar_conceitos("C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/Trabalho2/json/glossario_geral.json")
    return render_template("tabela.html", doencas=doencas)


app.run(host="localhost", port=4002, debug=True)
