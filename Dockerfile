FROM python:3.8-alpine

RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY combinedIngress combinedIngress
COPY main.py main.py
ENTRYPOINT ["python3", "main.py"]
