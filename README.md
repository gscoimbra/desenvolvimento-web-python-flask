# 📌 Projeto com Flask + PostgreSQL

Este é um projeto criado para fins de aprendizado, utilizando as tecnologias Python, Flask e PostgreSQL. A aplicação realiza operações de CRUD de usuários.

## 🚀 Tecnologias Utilizadas

- 🐍 Python 3
- 🌐 Flask
- 🐘 PostgreSQL
- 🎨 HTML (Jinja2 Templates)
- 💾 Psycopg2 (driver de conexão com PostgreSQL)

---

## ⚙️ Funcionalidades

- ✅ Cadastrar usuário (nome e e-mail)
- ✅ Listar usuários
- ✅ Editar usuário
- ✅ Remover usuário


---

## 📦 Como rodar

### 1. Clone o repositório:

```bash
git clone https://github.com/gscoimbra/desenvolvimento-web-python-flask.git
```

### 2. Instale as dependências:
```bash
pip install flask psycopg2
```

### 4. Atualize as credenciais de conexão no app.py:
```base
db = psycopg2.connect(
    host="localhost",
    dbname="api2-python",
    user="postgres",
    password="root"
)
```

### 5. Configure o Banco de Dados:
Crie um database chamado api2-python e execute:
```bash
CREATE TABLE usuarios (
  id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  nome VARCHAR(100),
  email VARCHAR(100),
);
```

### 6. Execute o projeto:
No terminal:
```bash
python app.py
```

## 🧪 Validações
- ✅ Campos obrigatórios: nome e email
- ✅ Campos com strip() para evitar espaços em branco
- ✅ Feedback simples por mensagem em caso de erro