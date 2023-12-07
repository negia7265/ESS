# https://dateparser.readthedocs.io/en/latest/introduction.html#search-for-dates-in-longer-chunks-of-text
from dateparser.search import search_dates
def extract_date(text):
    dates=search_dates(text)
    date=set()
    for d in dates:
        date.add(d[1].strftime("%d-%m-%Y"))
    return date

text='Thane Pune\nOne Way\ndec 13 2018 dec 13 2018\nGuest Details\n01. Yogesh Chhaproo'
print(extract_date(text))