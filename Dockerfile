FROM python:3.8-slim

COPY requirements.txt .
RUN apt-get update &&\
    apt-get install --no-install-recommends --yes build-essential

RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
COPY main.py /main.py

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]