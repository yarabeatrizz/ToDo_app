from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# ------------------ CONEXÃO BANCO ------------------
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
dbname = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{user}:{password}@{host}/{dbname}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ------------------ TABELA ------------------
class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    prioridade = db.Column(db.String(20))
    prazo = db.Column(db.Date)
    status = db.Column(db.String(20))


# ------------------ LOADING PAGE ------------------
@app.route("/")
def loading():
    return render_template("loading.html")


# ------------------ PÁGINA PRINCIPAL ------------------
@app.route("/tarefas")
def home():

    prioridade = request.args.get("prioridade")
    prazo = request.args.get("prazo")

    query = Task.query

    # filtro prioridade
    if prioridade and prioridade != "":
        query = query.filter(Task.prioridade == prioridade)

    # filtro data
    if prazo and prazo != "":
        try:
            data_formatada = datetime.strptime(prazo, "%Y-%m-%d").date()
            query = query.filter(Task.prazo == data_formatada)
        except:
            pass

    tarefas = query.all()

    return render_template("index.html", tarefas=tarefas)


# ------------------ PÁGINA NOVA TAREFA ------------------
@app.route("/nova")
def nova_tarefa():
    return render_template("nova.html")


# ------------------ ADICIONAR ------------------
@app.route("/adicionar", methods=["POST"])
def adicionar():

    nome = request.form["nome"]
    descricao = request.form.get("descricao")
    prioridade = request.form.get("prioridade")
    prazo = request.form.get("prazo")

    if prazo:
        prazo = datetime.strptime(prazo, "%Y-%m-%d").date()
    else:
        prazo = None

    nova = Task(
        nome=nome,
        descricao=descricao,
        prioridade=prioridade,
        prazo=prazo,
        status="pendente"
    )

    db.session.add(nova)
    db.session.commit()

    return redirect(url_for("home"))



# ------------------ EDITAR ------------------
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

    prazo = request.form.get("prazo")
    if prazo:
        tarefa.prazo = datetime.strptime(prazo, "%Y-%m-%d").date()

    tarefa.status = request.form.get("status")

    db.session.commit()
    return redirect(url_for("home"))



# ------------------ CONCLUIR ------------------
@app.route("/concluir/<int:id>")
def concluir(id):
    tarefa = Task.query.get_or_404(id)
    tarefa.status = "concluida"
    db.session.commit()
    return redirect(url_for("home"))



# ------------------ DELETAR ------------------
@app.route("/deletar/<int:id>")
def deletar(id):
    tarefa = Task.query.get_or_404(id)
    db.session.delete(tarefa)
    db.session.commit()
    return redirect(url_for("home"))



# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(debug=True)
