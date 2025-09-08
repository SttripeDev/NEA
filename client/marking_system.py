import math
from sentence_transformers import SentenceTransformer


class MarkingSystem:
    def __init__(self):
        self.model_name = "bert-base-nli-mean-tokens"
        self.model = SentenceTransformer(self.model_name)

    def marker(self,user_string,answer_string):
        vec_user , vec_actual = self.vectorise_sentence(user_string,answer_string)
        numerator_value = self.numerator(vec_user, vec_actual)
        a_norm = self.norms_calculation(vec_user)
        b_norm = self.norms_calculation(vec_actual)
        denominator_value = self.denominator(a_norm, b_norm)
        final = numerator_value / denominator_value

        if final > 0.7:
            return True
        else:
            return False

    def vectorise_sentence(self,user,actual):

        sentence_vectors = self.model.encode([user, actual])
        vec_user = sentence_vectors[0]
        vec_actual = sentence_vectors[1]
        return vec_user,vec_actual

    def numerator(self,a,b):
        # Calculate dot product
        total = 0
        x = 0
        for x in range(len(a)):
            dot_product = a[x] * b[x]
            total += dot_product
            x += 1
        return total

    def norms_calculation(self,vector):
        total = 0
        x = 0
        for x in range(len(vector)):
            squared = vector[x] ** 2
            total += squared

        total = math.sqrt(total)
        x += 1
        return total

    def denominator(self,a,b):
        similarity = a * b

        return similarity

if __name__ == "__main__":
    marking = MarkingSystem()
    user_sentence = "Hello World I am John"
    actual_sentence = "Why hello world I am called john"
    print(marking.marker(user_sentence,actual_sentence))