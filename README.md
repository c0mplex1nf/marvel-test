
# Marvel App

For this project i simulated three different microservices that are comunicating between then with the use of a event bus, basicly we got a Villain microservice, a Comic microservice and a Character microservice.
When we want to import the data from the Villain what we do first is create the Villain and after that, push an event to the event bus that is going to create a task to publish a message to a queue that another of our microservice is hearing and after create the Comic we do the same process for Characters
to demostrate better how it works im goign to attach a diagram

![alt text](https://i.ibb.co/7WbTN35/image-2023-03-29-092243726.png)
## Authors

- [@c0mplex1nf](https://github.com/c0mplex1nf)


## API Reference

#### Impor Villain

```http
  GET /villain/import/{villain_code}
```
Is possible to import any other villaib that exist in the marvel database just change the code

| Parameter | Type     | Description                | URL                       |
| :-------- | :------- | :------------------------- | :-------------------------------- |
| `villan_code` | `string` | **Required**. spectrum (example)  |http://localhost:8000/villain/import/spectrum |

#### Get Villain Related Characters

```http
  GET /villain/{villain_code}
```

| Parameter | Type     | Example                        | URL                       |
| :-------- | :------- | :-------------------------------- | :-------------------------------- |
| `villain_code`      | `string` | **Required**. spectrum  | http://localhost:8000/villain/spectrum|


## Deployment

To deploy this project run

```bash
  mv .env.example .env
```

```
  set your private and public marvel key in the file .env
```

```bash
  docker-compose build --no-cache
```

```bash
  docker-compose up -d

```

Just this all the other things are goign ot be generated at the moment the system goes up


## Roadmap

- There are some pattern that are missign because of time

- Implement Saga pattern

- Make integration test with the use of the queues

- Make agreggators for the entities

- Re use some parts of the code

- Make DTOS
## Appendix

For this project we are using different patterns like DDD, CQRS, Repository, Hexagonal, Clean Architecture and Event Source between others

![alt text](https://docs.google.com/drawings/d/e/2PACX-1vQ5ps72uaZcEJzwnJbPhzUfEeBbN6CJ04j7hl2i3K2HHatNcsoyG2tgX2vnrN5xxDKLp5Jm5bzzmZdv/pub?w=960&h=657)

## Tech Stack


**Server:** Python, FastApi

**Infra:**  Docker, Docker-compouse, Rabbitmq

**Libraries:**  fastapi, pydantic, uvicorn,
asyncio, SQLAlchemy, alembic, python-doten, requests, pika, aio_pika


## License

[MIT](https://choosealicense.com/licenses/mit/)