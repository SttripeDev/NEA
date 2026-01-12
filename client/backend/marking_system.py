import math
from sentence_transformers import SentenceTransformer

'''
Name: MarkingSystem
Purpose: Contains the code for marking user answers
'''
class MarkingSystem:
    '''
    Name: __init__
    Purpose: Constructor for default values for the marking system
    '''
    def __init__(self):
        self.model_name = "bert-base-nli-mean-tokens"
        self.model = SentenceTransformer(self.model_name)

    ''' 
    Name: marker
    Parameters: user_string: string , answer_string: string 
    Returns: True / False : Boolean 
    Purpose: Main process that calls upon the marking system to find vector value , and cosine similarity of them.
    '''
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
    ''' 
    Name: vectorise_sentence
    Parameters: user: string , actual: string 
    Returns: vec_user: array , vec_actual: array
    Purpose: Uses SBERT to convert sentences to vectors.
    '''
    def vectorise_sentence(self,user,actual):

        sentence_vectors = self.model.encode([user, actual])
        vec_user = sentence_vectors[0]
        vec_actual = sentence_vectors[1]
        return vec_user,vec_actual
    ''' 
    Name: numerator
    Parameters: a : integer, b: integer
    Returns: total: integer
    Purpose: calculates dot product for numerator of cosine similarity equation
    '''
    def numerator(self,a,b):
        # Calculate dot product
        total = 0
        x = 0
        for x in range(len(a)):
            dot_product = a[x] * b[x]
            total += dot_product
            x += 1
        return total
    ''' 
    Name: norms_calculator
    Parameters: vector: array
    Returns: total: integer
    Purpose: calculates the norm of the vector
    '''
    def norms_calculation(self,vector):
        total = 0
        x = 0
        for x in range(len(vector)):
            squared = vector[x] ** 2
            total += squared

        total = math.sqrt(total)
        x += 1
        return total
    ''' 
    Name: denominator
    Parameters: a: integer, b: integer
    Returns: denominator_value: integer
    Purpose: calculates the denominator (a*b)
    '''
    def denominator(self,a,b):
        denomitator_value = a * b

        return denomitator_value

if __name__ == "__main__":
    marking = MarkingSystem()
    user_sentence = "Hello World I am John"
    actual_sentence = "Why hello world I am called john"
    print(marking.marker(user_sentence,actual_sentence))