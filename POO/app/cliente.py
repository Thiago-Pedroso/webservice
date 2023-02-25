from app import app
from flask import request, render_template, flash
from jinja2 import Environment
import json
import os
from datetime import date

@app.route("/dash") 
def dash():
    return render_template('dash.html')


#-----------------------------------------------------------------------------
# INDEX
@app.route("/index") 
def pagina_inicial():
    return render_template('landing.html')

@app.route("/") 
def index():
    return render_template('pag_vendas.html')

@app.route("/cadastro") 
def pagina_cadastro():
    return render_template('cadastro.html')

#-----------------------------------------------------------------------------
# CADASTRO (Usuário)

@app.route("/cadastrar", methods=['POST'])
def cadastrar():
    user = []
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')
    user = [{
        "nome":usuario,
        "senha":senha
    }]
    with open('app/users.json') as users:
        arquivo = json.load(users)
    arquivo2 = arquivo + user
    with open('app/users.json', 'w') as arquivo:
        json.dump(arquivo2, arquivo, indent=4)
    return render_template("login.html")

#-----------------------------------------------------------------------------
# LOGIN (Usuário)
@app.route("/login", methods=['GET']) 
def login():
    return render_template('login.html')

@app.route("/logar", methods=['POST']) 
def logar():
    usuario = request.form['usuario']
    senha = request.form['senha']
    with open('app/users.json') as usuarios:
        lista = json.load(usuarios)
        contador = 0
        for i in lista:
            contador += 1
            if usuario == i['nome'] and senha == i['senha']:
                return render_template('sistema.html',usuario=usuario, senha=senha)
            if contador >= len(lista):
                return render_template('login_errado.html')    

#-----------------------------------------------------------------------------
# SISTEMA PDV
@app.route("/sistema")
def sistema():
    return render_template("sistema.html")

# Arrays para gravar dados
produtos = []
clientes = []
compra_json = []
produtos_json = []

# Cadastro de produtos
@app.route("/cadastrar_produto", methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        nome = request.form.get("nome")
        preco = request.form.get("preco")
        tipo = request.form.get("tipo")
        quantidade = request.form.get("quantidade")
        produtos_json = [{
            "nome": nome,
            "tipo": tipo,
            "preco": preco,
            "quantidade": quantidade,
            "total": float(preco) * float(quantidade)
        }]
        with open('app/produtos.json') as comp:
            arquivo = json.load(comp)
        arquivo2 = arquivo + produtos_json
        with open('app/produtos.json', 'w') as arquivo:
            json.dump(arquivo2, arquivo, indent=4)
        produtos.append({"nome": nome, "preco": preco, "quantidade": quantidade})
    return render_template("sistema.html", produtos=produtos, clientes=clientes)

@app.route("/cadastrar_compra", methods=['GET', 'POST'])
def cadastrar_compra():
    if request.method == 'POST':
        cpf = request.form.get("cpf")
        genero = request.form.get("genero")
        idade = request.form.get("idade")
        data = date.today()
        valor_total = 0

        #Abrindo json de produtos, pegando o valor somado de todos e depois deletando tudo
        lista_zerada = [{
            "nome": "nome",
            "tipo": "tipo",
            "preco": 0,
            "quantidade": 0,
            "total": 0
        }]
        with open('app/produtos.json') as prods:
            lista = json.load(prods)
            for produto in lista:
                valor_total += produto['total']
        arquivo2 = lista_zerada
        with open('app/produtos.json', 'w') as lista:
            json.dump(arquivo2, lista, indent=4)
        
        global produtos 
        produtos = []

        compra_json = [{
            "cpf":cpf,
            "genero":genero,
            "idade":idade,
            "valor":valor_total
        }]
        
        with open('app/compras.json') as comp:
            arquivo = json.load(comp)
        arquivo2 = arquivo + compra_json
        with open('app/compras.json', 'w') as arquivo:
            json.dump(arquivo2, arquivo, indent=4)
        clientes.append({"cpf": cpf, "genero": genero, "idade": idade, "valor_total": valor_total, "data": data})
    return render_template("sistema.html", clientes=clientes)
    

# Função personalizada para preço total de cada produto
@app.template_filter()
def preco_total(preco, quantidade):
    return float(preco) * float(quantidade)

app.add_template_filter(preco_total)

# Função personalizada para preço total da compra
def somar(lista):
    return sum(lista)

app.jinja_env.filters['soma'] = somar


