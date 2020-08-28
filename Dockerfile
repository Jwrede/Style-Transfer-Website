FROM python

WORKDIR /usr/src/app

RUN apt-get update &&\
  apt-get --assume-yes install ffmpeg

COPY . /usr/src/app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]