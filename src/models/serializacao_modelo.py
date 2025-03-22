import pickle as pkl
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

df = pd.read_csv("../../data/casas.csv")
colunas = ["tamanho", "ano", "garagem"]

x = df.drop("preco", axis=1)
y = df["preco"]
x_treino, x_teste, y_treino, y_teste = train_test_split(
    x, y, test_size=0.3, random_state=42
)
modelo = LinearRegression()
modelo.fit(x_treino, y_treino)

pkl.dump(modelo, open("modelo.pkl", "wb"))
