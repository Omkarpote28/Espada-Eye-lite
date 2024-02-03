FROM python:3.11.0
COPY . /Espada-Eye-lite
WORKDIR /Espada-Eye-lite
RUN pip install -r requirements.txt -v
EXPOSE $PORT
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT Espada-Eye-lite:Espada-Eye-lite
