from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
dbname = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{user}:{password}@{host}/{dbname}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Task(db.Model):
    __tablename__ = 'tasks'   # nome exato da tabela do MySQL

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    prioridade = db.Column(db.String(20))
    prazo = db.Column(db.Date)
    status = db.Column(db.String(20))

@app.route("/")
def home():
    tarefas = Task.query.all()
    return render_template("index.html", tarefas=tarefas)

# Listando as tarefas

@app.route("/tarefas")
def listar_tarefas():
    tarefas = Task.query.all()
    lista = []

    for t in tarefas:
        lista.append({
            "id": t.id,
            "nome": t.nome,
            "descricao": t.descricao,
            "prioridade": t.prioridade,
            "prazo": t.prazo.strftime("%y-%m-%d") if t.prazo else None,
            "status": t.status
        })
    return jsonify(lista)

# Adicionado nova Tarefa

@app.route("/adicionar", methods=["POST"])
def adicionar():
    nome = request.form["nome"]
    descricao = request.form.get("descricao")
    prioridade = request.form.get("prioridade")
    prazo = request.form.get("prazo")

    nova = Task(
        nome=nome,
        descricao=descricao,
        prioridade=prioridade,
        prazo=prazo,
        status="pendente"
    )

    db.session.add(nova)
    db.session.commit()

    return home()

# Função de Editar tarefa

@app.route("/editar/<int:id>")
def editar(id):
    tarefa = Task.query.get_or_404(id)
    return render_template("editar.html", tarefa=tarefa)

@app.route("/atualizar/<int:id>", methods=["POST"])
def atualizar(id):
    tarefa = Task.query.get_or_404(id)

    tarefa.nome = request.form["nome"]
    tarefa.descricao = request.form.get("descricao")
    tarefa.prioridade = request.form.get("prioridade")
    tarefa.prazo = request.form.get("prazo")
    tarefa.status = request.form.get("status")

    db.session.commit()
    return home()

# Função de Concluir tarefa 

@app.route("/concluir/<int:id>")
def concluir(id):
    tarefa = Task.query.get_or_404(id)
    tarefa.status = "concluida"
    db.session.commit()
    return home()

# Função de Deletar tarefa

@app.route("/deletar/<int:id>")
def deletar(id):
    tarefa = Task.query.get_or_404(id)
    db.session.delete(tarefa)
    db.session.commit()
    return home()



if __name__ == "__main__":
    app.run(debug=True)
