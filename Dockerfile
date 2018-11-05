FROM python:3.6
EXPOSE 5000
RUN pip install -r requirementes.txt
RUN python -m spacy download pt
RUN python populate.py
ENTRYPOINT ["python"]
CMD ["execute.py"]