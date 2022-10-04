## Setup

### DB migrations

```commandline
dbmate --url ${POSTGRES_URL} up
```

## Docker

```
docker build -t aiven:latest .
```

```commandline
docker run --env-file .env aiven aiven.producer
```

```commandline
docker run --env-file .env aiven aiven.consumer
```