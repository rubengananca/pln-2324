from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


filename = "conceitos.json"
with open(filename, 'r', encoding='utf-8') as file:
    conceitos = json.load(file)
    
def guardar_conceitos(conceitos, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(conceitos, file, ensure_ascii=False, indent=4)

@app.route("/")
def home():
    tamanho = len(conceitos)
    return render_template("home.html", tamanho = tamanho)


@app.route("/conceitos")
def listar_conceitos():
    return render_template("conceitos.html",conceitos = conceitos)

@app.route("/conceito/<designacao>") 
def consultar_conceitos(designacao):
    desig = conceitos[designacao]
    desig_pt = desig["desc"]
    desig_en = desig["en"]
    
    desig_fr = desig.get("fr") #Encontra o que está na chave, se a chave não existir tem o valor None
    desig_es = desig.get("es")
    desig_de = desig.get("de")
    
    return render_template("descricao.html",desig_pt = desig_pt, desig_en = desig_en, desig_es = desig_es, desig_de = desig_de, desig_fr = desig_fr, designacao = designacao)  
  
@app.route("/conceito/<designacao>/editar", methods=["GET", "POST"])
def editar_conceitos(designacao):
    global conceitos,filename
    
    if request.method == "GET":
        desig = conceitos[designacao]
        desig_pt = desig["desc"]
        desig_en = desig["en"]
        desig_fr = desig.get("fr") 
        desig_es = desig.get("es")
        desig_de = desig.get("de")
        return render_template("editar.html", designacao=designacao, desig_pt=desig_pt, desig_en=desig_en, desig_fr=desig_fr, desig_es=desig_es, desig_de=desig_de)
        
    elif request.method == "POST":
        desig_pt = request.form["desig_pt"]
        desig_en = request.form["desig_en"]
        nova_lingua = request.form["nova_lingua"]
        nova_descricao = request.form["nova_descricao"]
        
        if (nova_lingua not in conceitos[designacao]) and nova_lingua!="vazio" and nova_descricao!="":
            conceitos[designacao][nova_lingua] = nova_descricao
        elif nova_lingua in conceitos[designacao]: #atualiza
            conceitos[designacao][nova_lingua] = nova_descricao
        elif desig_pt:
            conceitos[designacao]["desc"] = desig_pt
        elif desig_en:
            conceitos[designacao]["en"] = desig_en
        elif desig_fr:
            conceitos[designacao]["fr"] = desig_fr
        elif desig_es:
            conceitos[designacao]["es"] = desig_es
        elif desig_de:
            conceitos[designacao]["de"] = desig_de

        guardar_conceitos(conceitos,filename) #guarda no json para quando voltar a abrir tar sempre atualizado
        return redirect(url_for("consultar_conceitos", designacao=designacao))



app.run(host="localhost",port=4002, debug = True)