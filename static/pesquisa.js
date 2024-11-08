function realizarPesquisa() {
    const termoPesquisa = document.getElementById('campo-pesquisa').value;
    
    if (termoPesquisa.trim() === "") {
        alert("Digite algo para pesquisar.");
        return;
    }

    fetch(`/pesquisar?query=${encodeURIComponent(termoPesquisa)}`)
        .then(response => response.json())
        .then(resultados => {
            const resultadosContainer = document.getElementById('resultados-pesquisa');
            resultadosContainer.innerHTML = '';  // Limpa os resultados anteriores

            if (resultados.length > 0) {
                resultados.forEach(item => {
                    const itemDiv = document.createElement('div');
                    itemDiv.classList.add('resultado-item');
                    itemDiv.innerHTML = `
                        <p><strong>Nome:</strong> ${item.nome}</p>
                        <p><strong>CPF/CNPJ:</strong> ${item.cpf_cnpj}</p>
                        <p><strong>Telefone:</strong> ${item.telefone}</p>
                        <p><strong>Email:</strong> ${item.email}</p>
                        <p><strong>Endereço:</strong> ${item.cidade}, ${item.bairro} - ${item.uf}</p>
                    `;
                    resultadosContainer.appendChild(itemDiv);
                });
            } else {
                resultadosContainer.innerHTML = "<p>Nenhum resultado encontrado.</p>";
            }
        })
        .catch(error => console.error("Erro ao realizar a pesquisa:", error));
}
