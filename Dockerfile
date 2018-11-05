FROM python:3.6
EXPOSE 5000

RUN adduser --disabled-login flask

WORKDIR /home/flask

COPY requirements.txt requirements.txt
COPY execute.py execute.py
COPY populate.py populate.py
COPY app app

RUN pip install -r ./requirements.txt
RUN python -m spacy download pt
RUN python populate.py

ENTRYPOINT ["python"]
CMD ["execute.py"]
