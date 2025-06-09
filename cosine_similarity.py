import math







class CosineSimilarity:

    def __init__(self):
        self.stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

    def cleanstring(self,string):
        string = string.lower()
        split_string = string.split(" ")
        for x in range(len(split_string)):
            for y in range(len(self.stop_words)):
                if split_string[x] == self.stop_words[y]:
                    split_string[x] = ""
                else:
                    continue
        return split_string

    def magnitude(self, ascii_array):
        mag = 0
        for x in range(len(ascii_array)):
            mag += ascii_array[x] ** 2
        return mag

    def cosine_calculation(self,string1, string2):
        # Convert strings to lowercase ASCII arrays
        ascii_array1 = [ord(char) for char in string1.lower()]
        ascii_array2 = [ord(char) for char in string2.lower()]

        # Extend shorter array with zeros to match length
        if len(ascii_array1) < len(ascii_array2):
            ascii_array1.extend([0] * (len(ascii_array2) - len(ascii_array1)))
        elif len(ascii_array2) < len(ascii_array1):
            ascii_array2.extend([0] * (len(ascii_array1) - len(ascii_array2)))

        # Calculate numerator (dot product)
        numerator = 0
        for x in range(len(ascii_array1)):
            numerator += ascii_array1[x] * ascii_array2[x]

        # Calculate magnitudes
        mag1 = self.magnitude(ascii_array1)
        mag2 = self.magnitude(ascii_array2)


        # Calculate denominator
        denominator = math.sqrt(mag1) * math.sqrt(mag2)

        # Calculate cosine similarity
        if denominator == 0:
            similarity = 0
        else:
            similarity = numerator / denominator

        return similarity

if __name__ == "__main__":
    CS = CosineSimilarity()
    test = "Hello My Name is John"
    test2 = "Hello My Name is Robert"
    cleaned1 = CS.cleanstring(test)
    cleaned2 = CS.cleanstring(test2)
    print(CS.cosine_calculation(test,test2))
