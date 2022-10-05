## Setup

### DB migrations

```commandline
dbmate --url ${POSTGRES_URL} up
```

## Docker

```
docker build --target base -t aiven:latest .
```

```commandline
docker run --env-file .env aiven aiven.producer
```

```commandline
docker run --env-file .env aiven aiven.consumer
```