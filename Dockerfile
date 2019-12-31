FROM python:3.7-buster

RUN apt update && apt install libc6 libatlas-base-dev -y

RUN pip3 install -i https://www.piwheels.org/simple numpy scipy

ARG PYTHON_FILE

ENV APP_MAIN_FILE=$PYTHON_FILE

COPY . .

RUN python -m unittest discover

ENTRYPOINT python ${APP_MAIN_FILE}
