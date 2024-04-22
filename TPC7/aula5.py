import shutil
from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

file = "conceitos.json"
with open(file, 'r', encoding='utf-8') as file:
    conceitos = json.load(file)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/conceitos")
def listar_Conceitos():
    return render_template("conceitos.html", conceitos = conceitos)

@app.route("/conceitos/<designacao>")
def consultar_Conceitos(designacao):
    if designacao in conceitos:
        conceito = conceitos[designacao]
        return render_template("conceito.html", conceito = conceito, designacao = designacao)
    else:
        return render_template("error.html", error = "Conceito não existe na nossa base de dados.")
        
    


@app.route("/conceitos", methods=["POST"])
def adicionar_conceitos():
    designacao = request.form.get("designacao")
    descricao = request.form.get("descricao")
    en = request.form.get("en")

    print(designacao,descricao,en)
    
    conceitos[designacao] = {
        "desc": descricao,
        "en": en
    }
    
    file_out1 = "conceitos.json"
    with open(file_out1, 'w', encoding='utf-8') as file_out1:
        json.dump(conceitos, file_out1, indent=4, ensure_ascii=False)
        
    file_out1.close()
    
    if "conceitos_backup.json" in os.listdir():
        file_out2 = "conceitos_backup.json" # O backup tambem tem de estar atualizado, nenhuma informação pode ser eliminada sem haver registo dela
        with open(file_out2, 'w', encoding='utf-8') as file_out2:
            json.dump(conceitos, file_out2, indent=4, ensure_ascii=False)
            
        file_out2.close()

    return render_template("conceitos.html", conceitos = conceitos)

@app.route("/conceitos/<designacao>", methods=["DELETE"])
def delete_conceitos(designacao):
    
    with open("conceitos.json", 'r', encoding='utf-8') as file:
        conceitos = json.load(file)
    
    # Verifica se o conceito com a designação fornecida existe
    if designacao in conceitos:
        # Realiza um backup do arquivo conceitos.json antes de fazer alterações
        shutil.copyfile("conceitos.json", "conceitos_backup.json")

        del conceitos[designacao]

        with open("conceitos.json", 'w', encoding='utf-8') as file_out: #guarda as alterações
            json.dump(conceitos, file_out, indent=4, ensure_ascii=False)
        
        return render_template("conceitos.html", conceitos=conceitos)
    else:
        return render_template("error.html", error="Conceito não existe na nossa base de dados.")

@app.route("/pesquisa")
def pesquisa():
    list_conceitos = []
    for conceito, detalhes in conceitos.items():
        desig = detalhes["desc"]
        en = detalhes["en"]
        conceito_str = f"{conceito}: {desig} ({en})"
        list_conceitos.append(conceito_str)
    return render_template("pesquisa.html", list_conceitos=list_conceitos)

@app.route("/tabela")
def table():
    global conceitos
    return render_template("tabela.html", conceitos=conceitos)

app.run(host="localhost", port=4002, debug=True)
