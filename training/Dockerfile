FROM python:3.7
COPY requirements.txt /requirements.txt
RUN ["pip3", "install", "-r", "requirements.txt"]

COPY /src /src
RUN ["python3", "src/train.py"]
