# Resource - https://stackoverflow.com/questions/15173225/calculate-cosine-similarity-given-2-sentence-strings
import math
import re
from collections import Counter
WORD = re.compile(r"\w+")

def cosine_similarity(text1,text2):
    vec1 = Counter(WORD.findall(text1))
    vec2 = Counter(WORD.findall(text2))
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0    
    return float(numerator) / denominator
    