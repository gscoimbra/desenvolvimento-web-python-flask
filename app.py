from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.config['VERSION'] = '1.0.0'

# Conexão global com PostgreSQL
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

@app.route('/deletar/<int:id>', methods=['POST'], endpoint='deletar_usuario')
def deletar(id):
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for("index"))

# API RESTful

@app.route("/api/usuarios", methods=["GET"])
def api_listar_usuarios():
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    lista = [{"id": u["id"], "nome": u["nome"], "email": u["email"]} for u in usuarios]
    return jsonify(lista)

@app.route("/api/usuarios/<int:id>", methods=["GET"])
def api_obter_usuario(id):
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    if usuario:
        return jsonify({"id": usuario["id"], "nome": usuario["nome"], "email": usuario["email"]})
    return jsonify({"erro": "Usuário não encontrado"}), 404

@app.route("/api/usuarios", methods=["POST"])
def api_cadastrar_usuario():
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    if not nome or not email:
        return jsonify({"erro": "Nome e email são obrigatórios"}), 400
    cursor.execute("INSERT INTO usuarios (nome, email) VALUES (%s, %s)", (nome, email))
    db.commit()
    return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201

@app.route("/api/usuarios/<int:id>", methods=["PUT"])
def api_editar_usuario(id):
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    if not cursor.fetchone():
        return jsonify({"erro": "Usuário não encontrado"}), 404
    cursor.execute("UPDATE usuarios SET nome = %s, email = %s WHERE id = %s", (nome, email, id))
    db.commit()
    return jsonify({"mensagem": "Usuário atualizado com sucesso"})

@app.route("/api/usuarios/<int:id>", methods=["DELETE"])
def api_deletar_usuario(id):
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    if not cursor.fetchone():
        return jsonify({"erro": "Usuário não encontrado"}), 404
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    db.commit()
    return jsonify({"mensagem": "Usuário deletado com sucesso"})

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == "__main__":
    app.run(debug=True)
