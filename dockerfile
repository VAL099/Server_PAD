# syntax=docker/dockerfile:1

FROM python:3.10.6

WORKDIR /server

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /server

EXPOSE 7100 7200
