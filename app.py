from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import cadastro

app = Flask(__name__)
app.secret_key = 'chave_secreta'  # Necessário para usar flash messages

# Rota para a página inicial (redireciona para login)
@app.route('/')
def home():
    return redirect(url_for('login'))  # Redireciona para a página de login

# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario_digitado = request.form['username']
        senha_digitada = request.form['password']
        
        # Chamando a função de verificação de login do cadastro.py
        if cadastro.verificar_login(usuario_digitado, senha_digitada):
            return redirect(url_for('cadastro_page'))  # Redireciona para a página de cadastro
        else:
            flash('Usuário ou senha incorretos. Tente novamente.')  # Exibe mensagem de erro
            return redirect(url_for('login'))  # Redireciona de volta para o login
    
    return render_template('login.html')  # Retorna a página de login para GET

# Rota para a página de cadastro e inserção de dados no banco
# Rota para a página de cadastro (GET) e inserção de dados no banco (POST)
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_page():
    if request.method == 'POST':
        # Recebe dados do formulário
        dados = request.form.to_dict()
        
        # Validação de CPF/CNPJ
        if not cadastro.verificacao_cpf_ou_cnpj(dados.get('cpf_cnpj')):
            return jsonify({'error': 'CPF ou CNPJ inválido.'}), 400
        
        # Inserir dados no banco
        id_cadastro = cadastro.inserir_dados_no_banco_cadastro(dados)
        if not id_cadastro:
            return jsonify({'error': 'CPF/CNPJ já cadastrado.'}), 400

        # Inserir dados de endereço, se houver
        if 'endereco' in dados:
            endereco = dados['endereco']
            cadastro.inserir_dados_no_banco_endereco(
                endereco["cidade"], endereco["bairro"], endereco["uf"], id_cadastro
            )
        
        return redirect(url_for('cadastro_page'))  # Redireciona de volta à página de cadastro após o envio
    
    return render_template('cadastro.html')  # Retorna a página de cadastro para GET


# Rota para pesquisa com paginação
@app.route("/pesquisa", methods=["GET", "POST"])
def pesquisa():
    termo_pesquisa = request.form.get("query") if request.method == "POST" else request.args.get("query", "")
    pagina = int(request.args.get("page", 1))
    
    resultados = cadastro.buscar_com_paginacao(termo_pesquisa, pagina=pagina) if termo_pesquisa else []
    return render_template("pesquisa.html", resultados=resultados, termo_pesquisa=termo_pesquisa)


if __name__ == '__main__':
    app.run(debug=True)
