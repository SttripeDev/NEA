from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SbertMarking:

    def __init__(self):
        self.model_name = "bert-base-nli-mean-tokens"
        self.model = SentenceTransformer(self.model_name)

    def marker(self, user, actual):
        sentence_vectors = self.model.encode([user, actual])

        vec_user = sentence_vectors[0].reshape(1, -1)
        vec_actual = sentence_vectors[1].reshape(1, -1)
        matches = cosine_similarity(vec_user, vec_actual)

        if matches >= 0.7:
            return True
        else:
            return False



if __name__ == "__main__":
    user_answer = "Hello my name is Johnathon"
    actual_answer = "Greetings my first name is Johnathon"
    SM = SbertMarking()
    SM.marker(user_answer, actual_answer)
