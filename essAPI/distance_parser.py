import re
def get_distance(text_arr):
    distance=0
    for text in text_arr:
        text=text.translate(str.maketrans('','','''()'''))
        #remove new line characters
        text=text.replace('\n', ' ')
        # lower case each letter of the word
        text=text.lower()
        # To ensure the match always starts with a number, use the \b word boundary anchor
        distance_regex=r'\b(\d+\.?\d*)[\s]*(km|kilomet|mile|meter|metre|foot|ft|yard|yd)'
        dist=re.findall(distance_regex,text)
        for i in dist:
            distance=max(distance,float(i[0]))                     
        distance_regex=r'\bdistance\s*(kms?|kilometers?|kilometres?|miles?|foot|yard|meters?|metres?)\s*(\d*\.?\d+)'
        dist=re.findall(distance_regex,text)
        for i in dist:
            distance=max(distance,float(i[1]))                     
    return distance
