import math


string1 = "Hello My Name is John"
string2 = "Hello My Name is Bob"


class CosineSimilarity:

    def __init__(self):
        self.extended = False
        self.numerator_total = 0
        self.denominator_total = 0
        self.ascii_array1 = []
        self.ascii_array2 = []

#Intital Steps
    def string_2_ascii_array(self, string):

        string = string.lower()
        ascii_string = [ord(char) for char in string]

        return ascii_string

    def extender(self, ascii_array1, ascii_array2):

        if len(ascii_array2) > len(ascii_array1):
            amount = len(ascii_array2) - len(ascii_array1)
            for x in range(amount):
                ascii_array1.append(0)
            self.extended = True
        elif len(ascii_array1) > len(ascii_array2):
            amount = len(ascii_array1) - len(ascii_array2)
            for x in range(amount):
                ascii_array2.append(0)
            self.extended = True
        else:
            self.extended = False

    def numerator_calc(self,ascii_array1,ascii_array2):

        for x in range(len(ascii_array2)):
            self.numerator_total = self.numerator_total + (ascii_array1[x] * ascii_array2[x])



    def magnitude(self,ascii_array):

        mag = None
        for x in range(len(ascii_array)):
            mag = mag + (ascii_array[x] ** 2)
        return mag

    def denominator_calc(self,magnitude_array1 ,magnitude_array2):

        denominator = math.sqrt(magnitude_array1) * math.sqrt(magnitude_array2)


    def run(self,string1,string2):
        self.ascii_array1 = CosineSimilarity.string_2_ascii_array(string1)
        self.ascii_array2 = CosineSimilarity.string_2_ascii_array(string1)













