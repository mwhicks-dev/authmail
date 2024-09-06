FROM python:3.10-bookworm
ARG TARGET=main
ARG CONFIG_PATH=src/authmail/config/

RUN apt install git -y
RUN mkdir /cert

RUN git clone https://github.com/mwhicks-dev/authmail

WORKDIR /authmail
RUN git checkout ${TARGET} && git pull
ADD ${CONFIG_PATH} /authmail/src/authmail/config/
RUN pip install -r src/authmail/requirements.txt
RUN pip install -r src/authmail/config/requirements.txt; return 0
RUN rm -rf src/authmail/config/*

WORKDIR /authmail/src/authmail
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0"]