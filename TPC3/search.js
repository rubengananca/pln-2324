function search() {
    var input = document.getElementById('searchInput').value.toLowerCase();
    var termos = document.getElementsByClassName('termo');

    var results = '<h2> Resultados: </h2> ';
    var hasResults = false;

    for (var i = 0; i < termos.length; i++) {
        var termoText = termos[i].textContent.toLowerCase();
        if (termoText.includes(input)) {
            results += termos[i].outerHTML;
            hasResults = true;
        }
    }

    if(!hasResults){
        results += "Nenhum resultado encontrado.";
    }else if(hasResults ==true && input==="" ){ // elimina as pesquisas feitas se o botão for clicado em vez de procurar por termos com espaços
        results = "";
        hasResults = false;
    }

    results += "<h2>  Dicionário </h2>"; 
    var searchResults = document.getElementById('searchResults');
    searchResults.innerHTML = results;
}

function refreshPage(){
    location.reload();
}
