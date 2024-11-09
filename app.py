from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import cadastro
import os


app = Flask(__name__)
app.secret_key = 'chave_secreta' 

'''Rotas que ligam as telas (login, cadastro e pesquisa)'''

@app.route('/')
def home():
    return redirect(url_for('login'))  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        usuario_digitado = request.form['username']
        senha_digitada = request.form['password']
        
        if cadastro.verificar_login(usuario_digitado, senha_digitada):
            return redirect(url_for('cadastro_page'))  
        else:
            flash('Usuário ou senha incorretos. Tente novamente.')  
            return redirect(url_for('login')) 
    
    return render_template('index.html') 

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_page():
    if request.method == 'POST':
        dados = request.form.to_dict()
        
        if not cadastro.verificacao_cpf_ou_cnpj(dados.get('cpf_cnpj')):
            return jsonify({'error': 'CPF ou CNPJ inválido.'}), 400
        
        id_cadastro = cadastro.inserir_dados_no_banco_cadastro(dados)
        if not id_cadastro:
            return jsonify({'error': 'CPF/CNPJ já cadastrado.'}), 400

        if 'endereco' in dados:
            endereco = dados['endereco']
            cadastro.inserir_dados_no_banco_endereco(
                endereco["cidade"], endereco["bairro"], endereco["uf"], id_cadastro
            )
        
        return redirect(url_for('cadastro_page'))
    
    return render_template('cadastro.html')

@app.route("/pesquisa", methods=["GET", "POST"])
def pesquisa():
    termo_pesquisa = request.form.get("query") if request.method == "POST" else request.args.get("query", "")
    pagina = int(request.args.get("page", 1))
    
    resultados = cadastro.buscar_com_paginacao(termo_pesquisa, pagina=pagina) if termo_pesquisa else []
    return render_template("pesquisa.html", resultados=resultados, termo_pesquisa=termo_pesquisa)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORTA", 5000)))

