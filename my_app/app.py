from modelo import recomendation
from flask import Flask, request, render_template

app = Flask(__name__)

# Lista de IDs de usuários
model = recomendation()
user_ids = model.ratings.userId.values

# Lista de IDs de filmes
movie_ids = model.movies.movieId.values 



@app.route("/")
def index():
    # Obtém o ID de usuário enviado na requisição
    user_id = request.args.get("user_id")
    print(user_id)
    # Verifica se o ID de usuário foi enviado na requisição
    if user_id is None:
        print('index')
        return render_template("index.html")

    # Converte o ID de usuário para inteiro
    user_id = int(user_id)

    # Verifica se o ID de usuário está na lista de IDs de usuários
    if user_id not in user_ids:
        return "Usuário inválido", 400

    recomendacao = model.recomendation(user_id)

    return render_template("result.html", user_id=user_id, lista_movies=recomendacao)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
