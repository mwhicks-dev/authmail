FROM python:3.10-bookworm
ARG TARGET=main

RUN apt install git -y

RUN git clone https://github.com/mwhicks-dev/authmail

WORKDIR /authmail
RUN git checkout ${TARGET} && git pull
RUN pip install -r src/authmail/requirements.txt
RUN pip install -r src/authmail/config/requirements.txt

WORKDIR /authmail/src/authmail
ENTRYPOINT uvicorn main:app --host 0.0.0.0 --port 8000