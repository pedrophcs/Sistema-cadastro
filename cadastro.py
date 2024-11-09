import requests
import bcrypt
import mysql.connector
from mysql.connector import Error

'''Conexão com o usuário'''
def verificar_login(usuario_digitado, senha_digitada):
    usuario = 'exemploLogado'
    senha = '1234'
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())

    if usuario_digitado == usuario and bcrypt.checkpw(senha_digitada.encode(), senha_hash):
        return True
    return False

def conectar_banco():
    try:
        connect = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="admin123",
            database="sistema_usuarios"
        )

        if connect.is_connected():
            return connect

    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

'''Validações de dados'''
def validate_cpf(cpf):

    digit_cpf = cpf.replace(".", "").replace("-", "")

    if len(digit_cpf) != 11 or not digit_cpf.isdigit():
        return False

    '''Primeiro verificador de digito'''
    multiplier = 10
    total = 0
    for number in digit_cpf[:9]:
        total += int(number) * multiplier
        multiplier -= 1
    digit_1 = (total * 10) % 11
    digit_1 = 0 if digit_1 >= 9 else digit_1

    '''Segundo verificador de digito'''
    multiplier = 11
    total = 0

    for number in digit_cpf[:9] + str(digit_1):
        total += int(number) * multiplier
        multiplier -= 1

    digit_2 = (total * 10) % 11
    digit_2 = 0 if digit_2 >= 9 else digit_2

    return digit_1 == int(digit_cpf[9]) and digit_2 == int(digit_cpf[10])

def validate_cnpj(cnpj):

    digit_cnpj = cnpj.replace(".", "").replace("-", "").replace("/", "")

    if len(digit_cnpj) != 14 or not digit_cnpj.isdigit():
        return False

    multipliers_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    multipliers_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    '''Primeiro dígito verificador'''
    total = sum(int(digit_cnpj[i]) * multipliers_1[i] for i in range(12))
    digit_1 = (total * 10) % 11
    digit_1 = 0 if digit_1 >= 10 else digit_1

    '''Segundo dígito verificador'''
    total = sum(int(digit_cnpj[i]) * multipliers_2[i] for i in range(13))
    digit_2 = (total * 10) % 11
    digit_2 = 0 if digit_2 >= 10 else digit_2

    return digit_1 == int(digit_cnpj[12]) and digit_2 == int(digit_cnpj[13])

def verificacao_cpf_ou_cnpj(cpf_cnpj):

    cpf_cnpj = cpf_cnpj.replace(".", "").replace("-", "").replace("/", "")
    print(f"CPF/CNPJ limpo: {cpf_cnpj}")

    if len(cpf_cnpj) == 11 and cpf_cnpj.isdigit():
        return validate_cpf(cpf_cnpj)
    elif len(cpf_cnpj) == 14 and cpf_cnpj.isdigit():
        return validate_cnpj(cpf_cnpj)
    else:
        return False

def cpf_cnpj_existe(cpf_cnpj, connect):

    cursor = connect.cursor()
    query = "SELECT COUNT(*) FROM cadastro WHERE cpf_cnpj = %s"
    cursor.execute(query, (cpf_cnpj,))
    (count,) = cursor.fetchone()
    return count > 0


'''Funções que coletam informações do usuário'''
def busca_cep(cep):
    cep = cep.replace(".", "").replace("-", "")
    if len(cep) == 8:
        link = f'https://viacep.com.br/ws/{cep}/json/'
        get_cep = requests.get(link)

        if get_cep.status_code == 200:
            dic_request = get_cep.json()
            uf = dic_request.get('uf', 'Não disponível')
            city = dic_request.get('localidade', 'Não disponível')
            address = dic_request.get('logradouro', 'Não disponível')
            neighborhood = dic_request.get('bairro', 'Não disponível')
            return uf, city, address, neighborhood
        else:
            print("Erro ao buscar o CEP")
            return False

    else:
        print('CEP inválido')
        return None

def obter_dados_usuario():
    nome = input('Nome completo: ')
    while True:
        cpf_cnpj = input('CPF ou CNPJ: ').replace(".", "").replace("-", "").replace("/", "")
        if verificacao_cpf_ou_cnpj(cpf_cnpj):
            print("CPF ou CNPJ válido")
            break
        else:
            print("CPF ou CNPJ inválido, tente novamente.")

    telefone = input('Telefone: ')
    email = input('Email: ')
    website = input('Website: ')
    atividade = input('Atividades econômicas ou profissionais: ')

    while True:
        cep = input('CEP: ')
        dados_cep = busca_cep(cep)
        if busca_cep(cep):
            print('CEP válido')
            break
        else:
            print("CEP inválido, tente novamente.")

    # Coleta os dados de endereço
    uf, city, address, neighborhood = dados_cep

    dados_usuario = {
        "nome": nome,
        "cpf_cnpj": cpf_cnpj,
        "telefone": telefone,
        "email": email,
        "website": website,
        "atividade": atividade,
        "endereco": {
            "uf": uf,
            "cidade": city,
            "bairro": neighborhood,
            "logradouro": address
        }
    }

    return dados_usuario


'''Movimentação com o banco de dados'''
def inserir_dados_no_banco_cadastro(dados_usuario):


    try:
        connect = conectar_banco()
        if connect.is_connected():
            cursor = connect.cursor()
            if cpf_cnpj_existe(dados_usuario["cpf_cnpj"], connect):
                print("Erro: CPF/CNPJ já cadastrado.")
                return None  # Não continua se CPF/CNPJ for duplicado
            
            cursor = connect.cursor()

        inserir_dados = """
        INSERT INTO cadastro (nome, cpf_cnpj, telefone, email, website, atividade)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        valores = (
            dados_usuario["nome"],
            dados_usuario["cpf_cnpj"],
            dados_usuario["telefone"],
            dados_usuario["email"],
            dados_usuario["website"],
            dados_usuario["atividade"]
        )

        cursor.execute(inserir_dados, valores)

        # Confirma a inserção
        connect.commit()

        id_cadastro = cursor.lastrowid
        print(f"{cursor.rowcount} registro(s) inserido(s) com sucesso.")

        return id_cadastro

    except Error as e:
        print("Erro ao conectar ou inserir dados no banco de dados:", e)

    finally:
        # Fechar o cursor e a conexão
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connect' in locals() and connect.is_connected():
            connect.close()
            print("Conexão ao banco de dados encerrada.")

def inserir_dados_no_banco_endereco(cidade, bairro, uf, id_cadastro):

    try:
        connect = conectar_banco()

        if connect.is_connected():
            cursor = connect.cursor()
  

        inserir_dados = """
        INSERT INTO endereco (cidade, bairro, uf, id_cadastro)
        VALUES (%s, %s, %s, %s)
        """


        cursor.execute(inserir_dados, (cidade, bairro, uf, id_cadastro))
        # Confirma a inserção
        connect.commit()
        print("Dados inseridos com sucesso!")

    
    except Error as e:
        print(f"Erro ao inserir dados: {e}")

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connect.is_connected():
            connect.close()
            print("Conexão ao MySQL encerrada.")

def buscar_com_paginacao(pesquisa, pagina=1, resultados_por_pagina=10):

    connect = conectar_banco()
    
    if connect.is_connected():
        cursor = connect.cursor(dictionary=True)  # Retorna como dicionário para fácil conversão a JSON
        offset = (pagina - 1) * resultados_por_pagina
        query = """
            SELECT * FROM cadastro
            JOIN endereco ON cadastro.idcadastro = endereco.id_cadastro
            WHERE LOWER(CONCAT_WS(' ', 
                    IFNULL(TRIM(nome), ''), 
                    IFNULL(TRIM(cpf_cnpj), ''), 
                    IFNULL(TRIM(telefone), ''), 
                    IFNULL(TRIM(email), ''), 
                    IFNULL(TRIM(cidade), ''), 
                    IFNULL(TRIM(bairro), ''), 
                    IFNULL(TRIM(uf), ''), 
                    IFNULL(TRIM(atividade), '')
                )) LIKE %s
            LIMIT %s OFFSET %s
        """
        parametro = f"%{pesquisa.lower()}%"
        cursor.execute(query, (parametro, resultados_por_pagina, offset))
        resultados = cursor.fetchall()
        
        cursor.close()
        connect.close()
        return resultados  # Retorna lista de dicionários como JSON
    else:
        return []