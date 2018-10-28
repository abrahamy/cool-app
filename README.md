# Cool App

A simple message processing app

## Requirements

### System

- Docker
- Docker Compose

### Python

- sqlalchemy
- psycopg2
- pandas
- pika

## Getting Started

- get

```
git clone https://github.com/abrahamy/cool-app.git
```

- start the consumer

```
cd cool-app
docker-compose build
docker-compose up
```

- run the producer (in another terminal from within the `cool-app` directory on the host computer)

```
export RABBITMQ_URI="amqp://cool_app:secret@localhost:5672/"
python -m cool_app producer data.csv
```

- verify that messages were persisted (password = secret)

```
docker-compose exec postgres bash
psql -U cool_app -d cool_app -W
select * from customers;
```
