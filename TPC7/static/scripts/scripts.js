
function delete_conceito(designacao){

    $.ajax({ 
        url: '/conceitos/' + designacao, 
        type: 'DELETE', 
        success: function (result) { 
            window.location.href = "/conceitos"
        } 
    }); 
}

$(document).ready( function () {
    $('#myTable').DataTable();
} );


// Função para pesquisar
$(document).ready(function(){
    $("#myInput").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#myconceitos li").filter(function() { // Seleciona os elementos âncora dentro de #myconceitos
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });
});
