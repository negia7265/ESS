import re
from dateparser.search import search_dates
from dateparser import parse

from dateparser_data.settings import default_parsers
parsers = [parser for parser in default_parsers if parser != 'relative-time']

def date_regex_check(pages):
    date_regex=[ r'\b(\d{1,2})\s*(\w{2})?\s*(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s*\d{4}',
                 r'\b(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s*(\d{1,2})\s*(\w{2})?\s*\d{4}'
               ]
    for text in pages:
        text=re.sub(r'[^\s\w]','',text)
        for pattern in date_regex:
            date=re.search(pattern, text)
            if date==None:
                continue
            date=date.group()
            date=parse(date).strftime("%d-%m-%Y")
            return date
    return None

def date_string_check(pages):
    for text in pages:
        index=text.find('date')
        if index==-1:
            continue
        date_len=len('date')
        date_string=' '.join(text[index+date_len:].split()[:10])
        dates = search_dates(text,settings={'STRICT_PARSING': True,'PARSERS': parsers,'DATE_ORDER': 'DMY'})
        if dates==None:
            continue
        for d in dates:
            return d[1].strftime("%d-%m-%Y")
    return None
def extract_date(pages):
    for text in pages:
        dates = search_dates(text,settings={'STRICT_PARSING': True,'PARSERS': parsers,'DATE_ORDER': 'DMY'})
        if dates==None:
            continue
        length=len(dates)
        date_string=dates[length-1][1].strftime("%d-%m-%Y")
        return date_string
    
def get_date(arr):
    for i in range(len(arr)):
        text=arr[i]
        text=text.lower()
        text=text.replace('\n',' ')
        text=text.translate(str.maketrans('','','''!"#%&'()*+;<=>,?@[]^`{}~$₹’'''))
        text=re.sub(r'[0-9]{6,20}', '', text)
        arr[i]=text
    date=date_regex_check(arr) 
    if date!=None:
        return date
    date=date_string_check(arr)
    if date==None:
        date=extract_date(arr)
    return date

