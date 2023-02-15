print("imports")
from modelo import recomendation
from flask import Flask, request, render_template
import random

app = Flask(__name__)
print("run app")
# Lista de IDs de usuários
model = recomendation()
user_ids = model.ratings.rating.values
print("modelo carregad")
# Lista de IDs de filmes
movie_ids = model.movies.movieId.values # -->  mapping de id de filme ?

# Função que retorna um ID de filme aleatório


@app.route("/")
def index():
    # Obtém o ID de usuário enviado na requisição
    user_id = request.args.get("user_id")
    print(user_id)
    # Verifica se o ID de usuário foi enviado na requisição
    if user_id is None:
        print('index')
        #return render_template("templates/index.html")
        return render_template("index.html")

    # Converte o ID de usuário para inteiro
    user_id = int(user_id)

    # Verifica se o ID de usuário está na lista de IDs de usuários
    if user_id not in user_ids:
        return "Usuário inválido", 400

    recomendacao = model.recomendation(user_id)

    #return render_template("templates/result.html", user_id=user_id, movie_name=recomendacao)
    return render_template("result.html", user_id=user_id, movie_name=recomendacao)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
