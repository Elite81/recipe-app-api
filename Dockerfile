FROM python:3.9-alpine3.13
LABEL mintainer='phrasium.com'

ENV PYTHONUNBUFFERED 1 


# copy our requirements.txt file into the docker image
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /temp/requirements.txt

#copy into our app derectory in the the app containter
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG  DEV=false

# Installing some dependencies unto our machine
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = 'true'] ; \
        then /py/bin/pip install -r /tmp/equirements.dev.txt ; \
    fi &&\
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user