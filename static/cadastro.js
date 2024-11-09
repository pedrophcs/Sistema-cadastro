document.getElementById("cadastroForm").addEventListener("submit", function(e) {
    e.preventDefault();

    const nome = document.getElementById("nome").value;
    const cpfCnpj = document.getElementById("cpf_cnpj").value;
    const telefone = document.getElementById("telefone").value;
    const email = document.getElementById("email").value;
    const website = document.getElementById("website").value;
    const atividade = document.getElementById("atividade").value; 

    // Dados que serão enviados ao servidor
    const dadosCadastro = {
        nome: nome,
        cpf_cnpj: cpfCnpj,
        telefone: telefone,
        email: email,
        website: website,
        atividade: atividade
    };

    // Enviar os dados para o backend (Flask)
    fetch('/cadastro', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dadosCadastro)
    })
    .then(response => response.json())
    .then(data => {
        alert("Cadastro realizado com sucesso!");
        
    })
    .catch(error => {
        console.error("Erro ao realizar o cadastro:", error);
        alert("Erro ao cadastrar. Tente novamente.");
    });
});
