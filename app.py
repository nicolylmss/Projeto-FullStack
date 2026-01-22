import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def conectar():
    return sqlite3.connect("database.db")

def criar_banco():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idade INTEGER,
        peso REAL,
        altura REAL,
        genero TEXT,
        atividade REAL,
        calorias REAL
    )
    """)

    conexao.commit()
    conexao.close()

criar_banco()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calcular", methods=["POST"])
def calcular():
    dados = request.json

    idade = int(dados["idade"])
    peso = float(dados["peso"])
    altura = float(dados["altura"])
    genero = dados["genero"]
    atividade = float(dados["atividade"])

    conexao = conectar()
    cursor = conexao.cursor()


    cursor.execute("""
    SELECT calorias FROM calculos
    WHERE idade=? AND peso=? AND altura=? AND genero=? AND atividade=?
    """, (idade, peso, altura, genero, atividade))

    resultado = cursor.fetchone()


    if resultado:
        conexao.close()
        return jsonify({
            "calorias": round(resultado[0]),
            "fonte": "banco de dados"
        })


    if genero == "masculino":
        tmb = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * idade)
    else:
        tmb = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * idade)

    calorias = tmb * atividade


    cursor.execute("""
    INSERT INTO calculos (idade, peso, altura, genero, atividade, calorias)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (idade, peso, altura, genero, atividade, calorias))

    conexao.commit()
    conexao.close()

    return jsonify({
        "calorias": round(calorias),
        "fonte": "novo cálculo"
    })

if __name__ == "__main__":
    app.run(debug=True)
