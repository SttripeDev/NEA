import math

def cosine_calculation(string1 , string2):
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
    mag1 = 0
    for x in range(len(ascii_array1)):
        mag1 += ascii_array1[x] ** 2

    mag2 = 0
    for x in range(len(ascii_array2)):
        mag2 += ascii_array2[x] ** 2

    # Calculate denominator
    denominator = math.sqrt(mag1) * math.sqrt(mag2)

    # Calculate cosine similarity
    if denominator == 0:
        similarity = 0
    else:
        similarity = numerator / denominator

    print(f"Cosine similarity: {similarity}")