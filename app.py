from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# Conexão com o PostgreSQL
db = psycopg2.connect(
    host="localhost",
    dbname="api2-python",
    user="postgres",
    password="root"
)

cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

@app.route("/")
def index():
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    return render_template("index.html", usuarios=usuarios)

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        email = request.form["email"].strip()

        if not nome or not email:
            return "Erro: Nome e Email são obrigatórios."

        cursor.execute("INSERT INTO usuarios (nome, email) VALUES (%s, %s)", (nome, email))
        db.commit()
        return redirect(url_for("index"))
    return render_template("cadastrar.html")

@app.route("/deletar/<int:id>")
def deletar(id):
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for("index"))

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if request.method == "POST":
        nome = request.form["nome"].strip()
        email = request.form["email"].strip()

        if not nome or not email:
            return "Erro: Nome e Email são obrigatórios."

        cursor.execute("UPDATE usuarios SET nome = %s, email = %s WHERE id = %s", (nome, email, id))
        db.commit()
        return redirect(url_for("index"))

    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    return render_template("editar.html", usuario=usuario)

@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        db.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Erro ao excluir: {e}"

if __name__ == "__main__":
    app.run(debug=True)