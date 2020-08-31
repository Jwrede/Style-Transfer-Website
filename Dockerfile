FROM python

WORKDIR /usr/src/app

RUN apt-get update &&\
  apt-get --assume-yes install ffmpeg

COPY . /usr/src/app

RUN pip install -r requirements.txt &&\
  pip install Flask gunicorn

EXPOSE 8080

CMD exec gunicorn --bind 0.0.0.0:8080 --workers 1 --threads 8 --timeout 0 app:app