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
    text=text.translate(str.maketrans('','',''',!"#%&'()*+-/:;<=>?@[\]^_`{|}~'''))
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

def extract_distance(text):
    token=preprocess_text(text)
    distance=set()
    km={'km','kilomet','kilometr'}
    pattern = re.compile('[0-9]*.?[0-9]+$')
    for i in range(len(token)-1):
      if pattern.match(token[i]) and token[i+1] in km:
          distance.add(float(token[i]))
    return distance


def extract_date(text):
    dates = list(datefinder.find_dates(text, strict=True))
    date=set()
    for d in dates:
        date.add(d.strftime("%d-%m-%Y"))
    return date

def extract_amount(text): #it's just a dummy function (need to write algorithms to extract amount accurately)
    starting_amount=re.search( r'[$₹]\s*(\d+\.?\d*)',text)
    cost=set()
    if starting_amount:
        cost.add(float(starting_amount.group(1)))
    return cost
