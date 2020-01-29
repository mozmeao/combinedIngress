FROM python:3.8-alpine

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY combinedIngress combinedIngress
COPY main.py main.py
ENTRYPOINT ["python3", "main.py"]

#RUN apk --update add --virtual build-dependencies python-dev build-base wget \
#  && pip install -r requirements.txt \
#  && python setup.py install \
#  && apk del build-dependencies