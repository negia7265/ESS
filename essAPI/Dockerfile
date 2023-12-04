FROM python:3

WORKDIR /app
COPY . /app
 
RUN pip install -r requirements.txt --root-user-action=ignore
RUN python download_nltk_corpora.py

EXPOSE 5000

CMD ["flask", "run"]