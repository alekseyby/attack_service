FROM python:3.10.0-slim-buster

ARG BASE_PATH=/opt/
ARG PROJECT_PATH=${BASE_PATH}django/

RUN apt-get update && apt-get install --no-install-recommends -y -o Acquire::ForceIPv4=true \
    build-essential \
    libpq-dev \
    postgresql-client \
    netcat \
    gettext \
    tzdata \
    vim \
&& apt-get clean

##########################################################################################################
#
#   Application requirements
#
##########################################################################################################

RUN pip3 install -U pip

RUN mkdir -p ${BASE_PATH}

COPY requirements.txt ${BASE_PATH}

RUN cd ${BASE_PATH} && pip3 install -r requirements.txt 

##########################################################################################################
#
#   Adding app files
#
##########################################################################################################

COPY ./ ${PROJECT_PATH}

COPY ./shell_scripts/ ${BASE_PATH}

RUN chmod +x ${BASE_PATH}*.sh

##########################################################################################################
#
#   For debug purposes only
#
##########################################################################################################

WORKDIR ${PROJECT_PATH}

RUN echo yes | python manage.py collectstatic
