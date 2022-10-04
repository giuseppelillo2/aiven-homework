FROM python:3.10-slim-bullseye AS base
ENV PIP_DEFAULT_TIMEOUT=100 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_NO_CACHE_DIR=1 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VERSION=1.1.14 \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  PYSETUP_PATH="/opt/pysetup" \
  PYTHONFAULTHANDLER=1 \
  PYTHONHASHSEED=random \
  PYTHONUNBUFFERED=1 \
  VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$VENV_PATH/bin:$PATH"
WORKDIR $PYSETUP_PATH

RUN pip install -U pip "poetry==$POETRY_VERSION"

RUN apt-get update && \
  apt-get install -y git software-properties-common build-essential gcc libssl-dev python3-dev make && \
  apt-get clean

# https://github.com/confluentinc/confluent-kafka-python/issues/1405#issuecomment-1209431553
RUN git clone https://github.com/edenhill/librdkafka /librdkafka
RUN cd /librdkafka && ./configure && make && make install && ldconfig
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

COPY certificates certificates
COPY aiven ./aiven
#RUN poetry build

# stage: production image
#FROM base AS production

#RUN apt-get update && \
#  apt-get install -y --no-install-recommends gcc librdkafka1 && \
#  apt-get clean

#COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

ENTRYPOINT ["python", "-m"]
CMD []

# stage: testing
FROM base AS testing
#
#RUN apt-get update && apt-get -y install --no-install-recommends make && rm -rf /var/lib/apt/lists/*
#RUN pip install -U pip "poetry==$POETRY_VERSION"
#
#COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH
#
RUN poetry install
#
COPY tests/ tests/
COPY Makefile Makefile
#
ENTRYPOINT ["make", "test"]
#CMD []