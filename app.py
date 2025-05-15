from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

usuarios = []  # Simula banco

@app.route("/")
def index():
    return render_template("index.html", usuarios=usuarios)

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        usuarios.append({"nome": nome, "email": email})
        return redirect(url_for("index"))
    return render_template("cadastrar.html")

@app.route("/deletar/<int:index>")
def deletar(index):
    if 0 <= index < len(usuarios):
        usuarios.pop(index)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
