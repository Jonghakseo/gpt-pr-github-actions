# Container image that runs your code
FROM python:3.8-slim

# Instalando as dependencias
COPY requirements.txt .
RUN apt-get update &&\
    apt-get install --no-install-recommends --yes build-essential
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh
COPY main.py /main.py

# Code file to execute when the docker container starts up (`entrypoint.sh`)
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]