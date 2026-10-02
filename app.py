from datetime import datetime
import sqlite3
from flask import Flask, g, redirect, render_template, request, url_for

app = Flask(__name__)
DATABASE = "database.db"


def get_db():
  db = getattr(g, "_database", None)
  if db is None:
    db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
  return db


@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, "_database", None)
  if db is not None:
    db.close()


def init_db():
  with app.app_context():
    db = get_db()
    db.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                prioridade TEXT NOT NULL, -- 'Normal' ou 'Preferencial'
                status TEXT NOT NULL, -- 'Aguardando', 'Em Atendimento', 'Concluído', 'Cancelado'
                data_criacao TEXT NOT NULL
            )
        """)
    db.commit()


# Inicializa o banco ao iniciar
init_db()


@app.route("/")
def index():
  db = get_db()
  fila = db.execute(
      "SELECT * FROM clientes WHERE status IN ('Aguardando', 'Em Atendimento')"
      " ORDER BY CASE WHEN prioridade = 'Preferencial' THEN 1 ELSE 2 END, id"
      " ASC"
  ).fetchall()
  return render_template("index.html", fila=fila)


@app.route("/adicionar", methods=["POST"])
def adicionar():
  nome = request.form.get("nome")
  prioridade = request.form.get("prioridade", "Normal")
  data_criacao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

  if nome:
    db = get_db()
    db.execute(
        "INSERT INTO clientes (nome, prioridade, status, data_criacao) VALUES"
        " (?, ?, 'Aguardando', ?)",
        (nome, prioridade, data_criacao),
    )
    db.commit()
  return redirect(url_for("index"))


@app.route("/chamar", methods=["POST"])
def chamar():
  db = get_db()
  # Finaliza o cliente que estava em atendimento (se houver)
  db.execute(
      "UPDATE clientes SET status = 'Concluído' WHERE status = 'Em Atendimento'"
  )

  # Pega o próximo da fila respeitando prioridade (Preferencial primeiro) e ordem de chegada (ID)
  proximo = db.execute(
      "SELECT id FROM clientes WHERE status = 'Aguardando' ORDER BY CASE WHEN"
      " prioridade = 'Preferencial' THEN 1 ELSE 2 END, id ASC LIMIT 1"
  ).fetchone()

  if proximo:
    db.execute(
        "UPDATE clientes SET status = 'Em Atendimento' WHERE id = ?",
        (proximo["id"],),
    )

  db.commit()
  return redirect(url_for("index"))


@app.route("/status/<int:id>/<string:novo_status>", methods=["POST"])
def alterar_status(id, novo_status):
  status_validos = ["Aguardando", "Em Atendimento", "Concluído", "Cancelado"]
  if novo_status in status_validos:
    db = get_db()
    db.execute(
        "UPDATE clientes SET status = ? WHERE id = ?", (novo_status, id)
    )
    db.commit()
  return redirect(url_for("index"))


@app.route("/historico")
def historico():
  db = get_db()
  clientes = db.execute(
      "SELECT * FROM clientes WHERE status IN ('Concluído', 'Cancelado') ORDER"
      " BY id DESC"
  ).fetchall()
  return render_template("historico.html", historico=clientes)


if __name__ == "__main__":
  app.run(debug=True)