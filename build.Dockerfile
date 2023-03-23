FROM python:3.8-slim

COPY requirements.txt .
RUN apt-get update &&\
    apt-get install --no-install-recommends --yes build-essential

RUN pip install -r requirements.txt

# docker build -f build.Dockerfile . -t unqocn/gpt-pr-github-actions:version --platform linux/amd64
# docker push unqocn/gpt-pr-github-actions:version