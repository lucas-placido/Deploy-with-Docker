import pandas as pd
import numpy as np
import json

caminho_movies = "data/movies.csv"
caminho_ratings = "data/ratings.csv"

class recomendation():
    def __init__(self, caminho_movies = caminho_movies, caminho_ratings = caminho_ratings):
        self.movies = pd.read_csv(caminho_movies)
        self.ratings = pd.read_csv(caminho_ratings).drop("timestamp", axis = 1)

    staticmethod
    def distance(x, y):
        return np.linalg.norm(x - y)

    def rating_user(self, id):
        return self.ratings.loc[self.ratings.userId == id][["movieId", "rating"]].set_index("movieId")

    def distance_users(self, id1, id2, minimo = 5): 
        user1 = self.rating_user(id1)
        user2 = self.rating_user(id2)
        users = user1.join(user2, how='inner', lsuffix='_user1', rsuffix='_user2')
        if len(users) < minimo:
            return None
        info = recomendation.distance(users.rating_user1, users.rating_user2)
        return (id1, id2, info)

    def one_vs_all(self, id, subset = None):
        user_rating = self.ratings.userId.unique()
        if subset:
            user_rating = user_rating[:subset]
        lista = [self.distance_users(id, user) for user in user_rating]
        lista = list(filter(None, lista))
        df = pd.DataFrame(lista, columns=["one", "all", "distance"])
        return df

    def closer(self, id1, subset = None, k_closest = 10):
        info = self.one_vs_all(id1, subset)
        info = info.sort_values(by="distance", ascending=True)
        info = info.set_index("all").drop(id1, axis = 0)
        return info.head(k_closest)

    def recomendation(self, id1, subset = None, k_closest = 10, recomendacoes = 10): # KNN

        closest = self.closer(id1, subset = subset, k_closest = k_closest)
        closest_users = closest.index 
        closest_rating = self.ratings.set_index("userId").loc[closest_users]

        recommends = closest_rating.groupby("movieId").mean()[["rating"]]
        recommends = recommends.sort_values("rating", ascending=False)
        recommends = recommends.merge(self.movies, left_on=recommends.index, right_on=self.movies.movieId).set_index("movieId").drop("key_0", axis = 1)
        final = recommends.head(recomendacoes)
        final = {id:str(titulo) for id, titulo in enumerate(final.title)}
        return final

if __name__ == "__main__":
    recomendation()