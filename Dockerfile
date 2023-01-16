FROM python:3.10.5-bullseye

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
