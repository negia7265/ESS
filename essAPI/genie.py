import datefinder
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re # For preprocessing
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
stop_words.remove('m')  #meter word must not be removed during preprocessing

def preprocess_text(text):
    #remove punctuation mark from the text
    text=text.translate(str.maketrans('','',''',!"#%&'()*+-/:;<=>?@[\]^_`{|}~$₹'''))
    #remove new line characters
    text=text.replace('\n', ' ')
    # lower case each letter of the word
    text=text.lower()
    #including space in beween {num}{word} 
    text=re.sub(r'(\d+)([a-z]+)', r'\1 \2', text)
    # split the words into tokens
    tokens=word_tokenize(text)
    # remove stop words 
    tokens = [word for word in tokens if word not in stop_words]
    #all words to root words
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    #lemmatization
    lemmatized = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized

# heuristic/logic based approach to distance extraction
def extract_distance(text):
    # it is necessary to preprocess text because distance could be written in 
    # format like 10Km , 10 kilometer, 30 kilometers ,etc. To convert it into 
    # root words and seperating number from word is necessary to extract distance.
    token=preprocess_text(text)
    distance=set()
    km={'km','kilomet','kilometr'} # found these three types of words for distance in invoice.
    # similarly meter, metres, m, miles etc can be used to extract distance .
    pattern = re.compile('[0-9]*.?[0-9]+$') # pattern to check for a number
    for i in range(len(token)-1):
      if pattern.match(token[i]) and token[i+1] in km:
          distance.add(float(token[i]))
    return distance

# used datefinder instead of dateparser because , dateparser is getting many dates 
# from invoice some are even incorrect. Best package found suitable is datefinder
# Although sometimes datefinder could mistake like if two times date is written 
# example: 18 march 2001 18 march 2001 then it is not able to parse date.
# out of all present packages datefinder is found to be the best
def extract_date(text):
    dates = list(datefinder.find_dates(text, strict=True))
    date=set()
    for d in dates:
        date.add(d.strftime("%d-%m-%Y"))
    return date