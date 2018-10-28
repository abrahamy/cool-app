FROM python:3

LABEL Author="Abraham Yusuf <aaondowasey@gmail.com>"

ARG LOG_FILE
ARG RABBITMQ_URI
ARG DATABASE_URI

ENV LOG_FILE=${LOG_FILE}}
ENV RABBITMQ_URI=${RABBITMQ_URI}
ENV DATABASE_URI=${DATABASE_URI}

# install dependencies
RUN apt-get -q -y update \
  && apt-get -q -y upgrade \
  && apt-get -q -y install libpq-dev \
  && apt-get -q clean \
  && python -m pip install --upgrade pip \
  && pip install poetry

# build cool-app package
COPY . /usr/src/cool-app
RUN cd /usr/src/cool-app \
  && poetry build \
  && pip install --upgrade dist/*.whl \
  && cd && rm -rf /usr/src/cool-app \
  && which cool_app

CMD [ "/usr/local/bin/cool_app", "consumer" ]