# Sistema de Cadastro

Este projeto é um Sistema de Cadastro desenvolvido como parte do portfólio de Pedro Henrique. O sistema foi criado utilizando **Python**, **MySQL** e **Flask** no backend, e **HTML**, **CSS** e **JavaScript** no frontend. O objetivo principal é gerenciar o cadastro de usuários com validação de dados e exibir pesquisas de forma eficiente.

## Funcionalidades

- **Autenticação de Usuário**: Login seguro com verificação de senha.
- **Cadastro de Usuários**: Formulário para inserir informações como nome, CPF/CNPJ, telefone e outras informações pertinentes.
- **Validação de Dados**: Verificação de CPF/CNPJ para evitar duplicações.
- **Pesquisa com Paginação**: Tela dedicada à pesquisa de registros com filtragem de resultados.
- **Responsividade**: O sistema é acessível em dispositivos móveis e desktop.
  
## Tecnologias Utilizadas

- **Backend**: Python, Flask, MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Segurança**: Biblioteca bcrypt para hash de senhas
- **Controle de Versão**: Git, com repositório no GitHub


## Pré-requisitos

1. **Python 3.x** e **pip** instalados.
2. **MySQL** instalado e configurado.
3. Pacotes necessários listados no arquivo `requirements.txt`:


## Configuração do Banco de Dados

1. Crie um banco de dados MySQL para o projeto:
```sql
CREATE DATABASE sistema_cadastro;

Crie as tabelas necessárias, conforme especificado no arquivo cadastro.py.

Configure as credenciais do banco no arquivo cadastro.py, na função conectar_banco().

Como Rodar o Projeto
Clone o repositório:

git clone https://github.com/seuusuario/sistema-cadastro.git

Instale os pacotes:

pip install -r requirements.txt

Execute a aplicação:

python app.py

Acesse o sistema em http://127.0.0.1:5000.

Como Usar
Login: Acesse a página de login para autenticação.
Cadastro: Após o login, utilize o formulário de cadastro para adicionar novos registros.
Pesquisa: Utilize a tela de pesquisa para buscar registros pelo nome, CPF/CNPJ ou outras informações.