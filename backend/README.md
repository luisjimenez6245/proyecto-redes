# Base-fastapi-API

The api arquitecture is based on the good practices for Fast-API by @tialongo, for more information check https://fastapi.tiangolo.com
## API Reference

All the models should have the same acces methods, you should check 
http://localhost:8000/docs for testings all the methods

#### Get all items

```http
  GET /items
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token` | `string` | **Required**. Your API key |

#### Get item

```http
  GET /api/items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |



#### Post Item

```http
  POST /items/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |



#### Put Item

```http
  PUT /items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |




#### Delete Item

```http
  DELETE /items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |



## Run Locally

Clone the project

```bash
  git clone ${project_link}
```

Go to the project directory

```bash
  cd ${project_name}
```

Create a virutal environment 

```bash
  virutalenv venv
```

Activate the virutalenv

```bash
  . ./venv/bin/activate
```


Install dependencies

```bash
  python3 -m pip install -r requirements.txt
```

Update the db

```bash
  alembic revision --autogenerate -m "made some changes"
  alembic upgrade head 
```

Start the server

```bash
  cd app
  python3 main.py
```

Start the celery server

```bash
  cd app
  celery -A celery_app worker -B -l info 
```

  
## Deployment

To deploy this project run

```bash
    ./install.sh
```

  
## Documentation

[Documentation](https://linktodocumentation)

  
## License

The project is licensed only for the use by the team.

  
