import math

stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]



    # - got two lists
    # - Iterate through split_string and compare against the entirety of stop words
    # - When one is found remove it replace with None value or something
def cleanstring(string):
    string = string.lower()
    split_string = string.split(" ")
    for x in range(len(split_string)):
        for y in range(len(stop_words)):
            if split_string[x] == stop_words[y]:
                split_string[x] = ""
            else:
                continue
    print(split_string)



def magnitude(array):
    mag = 0
    for x in range(len(array)):
        mag += array[x] ** 2
    return mag

def cosine_calculation(string1, string2):
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
    mag1 = magnitude(ascii_array1)
    mag2 = magnitude(ascii_array2)


    # Calculate denominator
    denominator = math.sqrt(mag1) * math.sqrt(mag2)

    # Calculate cosine similarity
    if denominator == 0:
        similarity = 0
    else:
        similarity = numerator / denominator

    print(f"Cosine similarity: {similarity}")

if __name__ == "__main__":
    sentence = "The Main idea that I had was to make maths great"
    cleanstring(sentence)
