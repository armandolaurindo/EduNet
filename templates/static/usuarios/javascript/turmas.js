function exibirForm(tipo){
    ver_lista_turma = document.getElementById('ver-lista-da-turma');
    ver_desempenho_turma = document.getElementById('ver-desempenho-da-turma');

    if(tipo == "1"){
        ver_lista_turma.style.display = "block";
        ver_desempenho_turma.style.display = "none";
    }else if(tipo == "2"){
        ver_desempenho_turma.style.display = "block";
        ver_lista_turma.style.display = "none";
    }
}

const openButtons = document.querySelectorAll('.open-modal')

openButtons.forEach(button => {
   button.addEventListener('click', () =>{
      
      const modaID = button.getAttribute('data-modal');
      const modal = document.getElementById(modaID);
      
      modal.showModal();
      
   });
});

const closeButtons = document.querySelectorAll('.close-modal')

closeButtons.forEach(button => {
   button.addEventListener('click', () =>{
     
      const modaID = button.getAttribute('data-modal')
      const modal = document.getElementById(modaID)

      modal.close()

   })
})

function attNota(notaID){
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
    id_nota = notaID

    data = new FormData()
    data.append('id_nota', id_nota)

    fetch("/atualizar_nota/",{
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data
    }).then(function(result){
        return result.json()
    }).then(function(data){
        inputNota = document.getElementById('att_nota')
        inputNota.value = data['nota']['nota']

        id = document.getElementById('id-Nota')
        id.value = id_nota

    })
}

function updateNota(){

    valorNota = document.getElementById('att_nota').value
    nota_id = document.getElementById('id-Nota').value

    fetch('/update_nota/' + nota_id,{

        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({
            nota: valorNota,
        })

    }).then(function(result){
       return result.json()
    }).then(function(data){
        console.log(data)
        if(data['status'] == '200'){
            nota = data['nota']
            alert('Nota alterada com sucesso')
        }else{
            alert('Ocorreu algum erro no processo')
        }
    })

}
/*
function dados_aluno(){

    btn_editar = document.getElementById('btn-editar')

    if(btn_editar.value == 'Editar'){
        aluno = document.getElementById('aluno_edit')
        console.log(aluno)
        csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
        id_a = aluno.value

        data = new FormData()
        data.append('id_aluno', id_a)

        fetch("/atualizar_aluno/",{
            method: "POST",
            headers: {
                'X-CSRFToken': csrf_token,
            },
            body: data
        }).then(function(result){
            return result.json()
        }).then(function(data){

            console.log(data)
            tb_num_matricula = document.getElementById('td-matricula')

            tb_nome = document.getElementById('tb-nome')

            tb_sobrenome = document.getElementById('tb-sobrenome')

            
            btn_editar.value = 'Salvar'
            console.log(btn_editar)

            tb_num_matricula.innerHTML = `<input value='${data['aluno']['numero_matricula']}' type='text' required class='form-control' placeholder='Ex:. 2025' name='att_num_marticula' id='att_num_marticula'>`

            tb_nome.innerHTML = `<input value='${data['aluno']['nome']}' type='text' required class='form-control' placeholder='Ex:. Joe' name='att_nome' id='att_nome'>`

            tb_sobrenome.innerHTML = `<input value='${data['aluno']['sobrenome']}' type='text' required class='form-control' placeholder='Ex:. Joe' name='att_sobrenome' id='att_sobrenome'>`
            

        })
    }if(btn_editar.value == 'Salvar'){
        console.log(btn_editar)
        att_num_marticula = document.getElementById('att_num_marticula').value

        att_nome = document.getElementById('att_nome').value
        
        att_sobrenome = document.getElementById('att_sobrenome').value

        console.log(id_a, csrf_token)
        console.log(att_num_marticula)
        console.log(att_nome)
        console.log(att_sobrenome)

        fetch('/update_aluno/' + id_a, {

            method: 'POST',
            headers: {
                'X-CSRFToken': csrf_token,
            },
            body: JSON.stringify({
                nome: att_nome,
                sobrenome: att_sobrenome,
                numero_matricula: att_num_marticula,
            })

        }).then(function(result){
           return result.json()
        }).then(function(data){
            console.log(data)
            if(data['status'] == '200'){
                nome = data['nome']
                sobrenome = data['sobrenome']
                numero_matricula = data['numero_matricula']
                alert('Dados alterados com sucesso')
            }else{
                alert('Ocorreu algum erro no processo')
            }
        })

    }
    
}*/
