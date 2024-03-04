import re

filename = "dicionario_medico.txt"

with open(filename, 'r', encoding='utf-8') as file:
    text = file.read()

# --- Substitui as quebras de página
text = re.sub(r"[^\f]\n\f", r"\n", text) 

# --- Marcar as designações
text = re.sub(r"\n\n(.+)",r"\n\n@\1",text)


# --- Extrair informação

termos = []
termos = re.findall(r"@(.+)\n([^@]+)",text) 
 
# --- Gerar HTML

def gerar_html(termos):
    
    html = ''
    for termo in termos:
        html += f"<div class='termo'><h4>Designação: {termo[0]}</h4>"
        html += f"<p> <b> Descrição: </b> {termo[1]}</p></div>"
        html += "<hr/>"

    return html

html_content = gerar_html(termos)

html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;1,500&display=swap" rel="stylesheet">
    
    <link rel="stylesheet" href="style.css">
    <title>Dicionário Médico</title>
</head>
<body>
  
  <div class="header">
    <button class="botao-header" onclick="refreshPage()"> Dicionário Médico <button> </div>
      
  <div class="corpo"> 
    <h2> Este dicionário médico foi desenvolvido para a disciplina de PLN </h2>

    <input type="text" class="barra" id="searchInput" placeholder="Pesquisar termo...">
    <button class="botao" onclick="search()">Pesquisar</button>
  
    <div id="searchResults" class="resultados"> 
    </div>

    {html_content}

  </div>

  <script src="search.js"></script>
</body>
</html>
"""

with open("site.html", "w", encoding='utf-8') as file_out:
    file_out.write(html_template)





    
    
