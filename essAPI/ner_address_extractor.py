from flair.data import Sentence
from flair.nn import Classifier
from flair.models import SequenceTagger
import json
tagger = SequenceTagger.load('ner-large-model')
cities=json.load('location.json')

states = ["rajasthan", "karnataka", "uttarakhand", "andhra pradesh", "arunachal pradesh", "assam", "bihar", "chhattisgarh", "goa", "gujarat", "haryana", "himachal pradesh", "jharkhand", "kerala", "madhya pradesh", "maharashtra", "manipur", "meghalaya", "mizoram", "nagaland", "odisha", "punjab", "rajasthan", "sikkim", "tamil nadu", "telangana", "tripura", "uttar pradesh", "west bengal", "jammu and kashmir", "ladakh", "andaman and nicobar islands", "chandigarh", "dadra and nagar haveli and daman and diu", "lakshadweep", "delhi", "puducherry"]

def IndiaExist(temp):
    for i in range(len(temp)):
        if (temp[i] == "India"):
            return True

def CityExist(city):
    for i in range(len(cities)):
        if (cities[i] == city):
            return True

def StateExist(state):
    for i in range(len(states)):
        if (states[i] == state):
            return True

def get_address(text):
    # Address Fetching
    sentence = Sentence(text)

    # run NER over sentence
    tagger.predict(sentence)
    
    # Extract tokens labeled as 'LOC' from the named entities
    loc_tokens = [str(entity) for entity in sentence.get_spans(
        'ner') if 'LOC' in str(entity.labels[0])]

    # Print the list of 'LOC' tokens
    loc_texts_inside_quotes = [re.search(r'"([^"]*)"', loc_token).group(1) for loc_token in loc_tokens]
    list_again = []
    if (IndiaExist(loc_texts_inside_quotes)):
        for i in range(len(loc_texts_inside_quotes)):
            if (loc_texts_inside_quotes[i] == "India"):
                list_again.append(i)
    else:
        for i in range(len(loc_texts_inside_quotes)):
            if (CityExist(loc_texts_inside_quotes[i])):
                list_again.append(i)

    if len(list_again) >= 1:
        # Extract the substring from the beginning to the first occurrence of "India"
        substring_before_first_india = loc_texts_inside_quotes[:list_again[0] + 1]

        # Extract the substring from the first occurrence of "India" to the second occurrence of "India"
        if len(list_again) >= 2:
            substring_between_indias = loc_texts_inside_quotes[list_again[0] + 1:list_again[1]+1]
        else:
            substring_between_indias = loc_texts_inside_quotes[list_again[0] + 1:]

    # removing white spaces

    cleaned_first_address = [word.strip()
                                for word in substring_before_first_india if word.strip()]
    cleaned_second_address = [word.strip()
                                for word in substring_between_indias if word.strip()]
    first_address = ', '.join(cleaned_first_address)
    second_address = ', '.join(cleaned_second_address)
    # Print the combined string
    return {'source': first_address, 'destination': second_address, 'date': unique_date, 'distance': unique_distance, 'cost': amount}
