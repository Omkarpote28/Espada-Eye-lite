FROM python:3.11.0
COPY . /Espada-Eye-v1.0
WORKDIR /Espada-Eye-v1.0
RUN pip install -r requirements.txt
EXPOSE $PORT
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT Espada-Eye-lite:Espada-Eye-lite
