function searchResponse(){
    try{
        const input = document.getElementById("searchFilter");
        location.href = `/crur/response/${input.value}`;
    }catch{
        alert("Aconteceu um erro no sistema, avise o setor de TI")
    }
}


function DeleteArchive(pk){
    let text = "Você realmente quer deletar o arquivo?";
    if (confirm(text) == true) {
        fetch(`/crur/archives/${pk}`, {
            method: 'PUT',
        })
        .then((response)=>{
            if(response.status == 200){
                alert("Arquivo deletado, pagina reiniciando!");
                window.location.reload();
            }else{
                alert("Algum erro ao deletar o arquivo, fale com o TI")
            }
        })
        .catch(()=>{
            alert("Algum erro ao deletar o arquivo, fale com o TI")
        })
    }
}


function uploadArchive(fileName, file, pk){
    const formData = new FormData();
    formData.append('desc', fileName);
    formData.append('file', file);
    fetch(`/crur/archives/${pk}`, {
        method: 'POST',
        body: formData
    })
    .then((response)=>{
        if(response.status == 200){
            alert("Arquivo upado, pagina reiniciando!");
            window.location.reload();
        }else{
            alert("Algum erro ao upar o arquivo, fale com o TI")
        }
    })
    .catch(()=>{
        alert("Algum erro ao upar arquivo, fale com o TI")
    })
}


function eventButton(e, element, inputFile, textInput, pk){
    const fileName = textInput.value;
    if(!fileName || fileName == "") return alert("Escreva um descrição");
    if(inputFile.files.length < 0) return;
    const file = inputFile.files[0];
    uploadArchive(fileName, file, pk);
    inputFile.value = '';
    element.style.display = "none";

}

function eventInput(e, element, btn, textInput){
    if(element.files.length > 0){
        btn.style.display = "block";
        textInput.style.display = "block";
        textInput.value = "";
    }else{
        btn.style.display = "none";
        textInput.style.display = "none";
    }
}


function configPage(){
    var inputs = document.getElementsByName("inputFile");
    inputs.forEach(input=>{
        const pk = input.getAttribute('data-pk');
        const btn = document.getElementById(`btn-${pk}`);
        const textInput = document.getElementById(`input-${pk}`);
        if(btn) btn.addEventListener('click', (e)=> eventButton(e, btn, input, textInput, pk));
        input.addEventListener("change", (e)=> eventInput(e, input, btn, textInput));
    })

}

window.addEventListener('DOMContentLoaded', (e)=>{
    configPage();
})