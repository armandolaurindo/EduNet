let tipo = document.getElementById('select1')


function exibir_form(){
    form_professor = document.getElementById('form_professor');
    form_encarregado = document.getElementById('form_encarregado');

    if(tipo.value == "P"){
        console.log(tipo.value)
        form_encarregado.style.display = "none";
        form_professor.style.display = "block";
    }else if(tipo.value == "E"){
        console.log(tipo.value)
        form_encarregado.style.display = "block";
        form_professor.style.display = "none";
    }
}
