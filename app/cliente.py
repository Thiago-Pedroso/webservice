from app import app
from flask import request, render_template, flash
from jinja2 import Environment

@app.route("/dash") 
def dash():
    return render_template('dash.html')


#-----------------------------------------------------------------------------
# INDEX
@app.route("/") 
def index():
    return render_template('landing.html')

#-----------------------------------------------------------------------------
# LOGIN
@app.route("/login", methods=['GET']) 
def login():
    return render_template('login.html')

usuarios = {
    'Thiago': 'thiago123',
    'Hugo': 'hugo123',
    'Vinicius': 'vinicius123',
    'Jorge': 'jorge123'	
}

@app.route("/logar", methods=['POST']) 
def logar():
    usuario = request.form['usuario']
    senha = request.form['senha']
    if usuario in usuarios and usuarios[usuario] == senha:
        return render_template('sistema.html',usuario=usuario, senha=senha)
    else:
        return render_template('login_errado.html')

#-----------------------------------------------------------------------------
# SISTEMA PDV
@app.route("/sistema")
def sistema():
    return render_template("sistema.html")

# Cadastro de produtos
produtos = []

@app.route("/cadastrar", methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form.get("nome")
        preco = request.form.get("preco")
        quantidade = request.form.get("quantidade")
        produtos.append({"nome": nome, "preco": preco, "quantidade": quantidade})
    return render_template("sistema.html", produtos=produtos)

# Função personalizada para preço total de cada produto
@app.template_filter()
def preco_total(preco, quantidade):
    return float(preco) * float(quantidade)

app.add_template_filter(preco_total)

# Função personalizada para preço total da compra
def somar(lista):
    return sum(lista)

app.jinja_env.filters['soma'] = somar


