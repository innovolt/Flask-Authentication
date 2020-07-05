FROM python:3.6


RUN mkdir /app

COPY . /app


EXPOSE 5000

WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "server.py"]
