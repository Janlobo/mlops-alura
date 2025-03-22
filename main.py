from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
from googletrans import Translator
import pickle as pkl
from dotenv import load_dotenv
import os

load_dotenv()
colunas = ["tamanho", "ano", "garagem"]
# Carregando o modelo
modelo = pkl.load(open("../../models/modelo.pkl", "rb"))

app = Flask(__name__)
app.config["BASIC_AUTH_USERNAME"] = os.getenv("BASIC_AUTH_USERNAME")
app.config["BASIC_AUTH_PASSWORD"] = os.getenv("BASIC_AUTH_PASSWORD")

basic_auth = BasicAuth(app)


# Definindo a routa que será acessada
@app.route("/")
def home():
    return "Olá, mundo!"


@app.route("/sentimento/<frase>")
@basic_auth.required
def sentimento(frase):
    # Traduzindo a frase para o inglês
    translator = Translator()
    tb_en = translator.translate(text=frase, src="auto", dest="en")

    # Analisando o sentimento da frase
    tb = TextBlob(tb_en.text)
    polaridade = tb.sentiment.polarity
    return f"Polaridade: {polaridade}"


@app.route("/prever/<int:tamanho>,<int:ano>,<int:garagem>")
def prever(tamanho, ano, garagem):
    tamanho = float(tamanho)
    ano = float(ano)
    garagem = float(garagem)
    preco = modelo.predict([[tamanho, ano, garagem]])[0]
    return f"Preço: {preco:.2f}"


@app.route("/cotacao/", methods=["POST"])
@basic_auth.required
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input])
    return jsonify({"preco": preco[0]})


# Iniciando o servidor
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
