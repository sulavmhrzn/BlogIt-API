
# BlogIt API 
Backend REST API for a blogging application using [Django Rest Framework](https://www.django-rest-framework.org/)


## Installation

**Configre Environment variables**
```
DJANGO_SECRET_KEY=
DEBUG=
   
POSTGRES_DATABASE_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
  
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_PORT=

```
**Activate virtual environment and Install requirements**

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Configure SMTP Email server [smtp4dev](https://github.com/rnwood/smtp4dev)**
```bash
docker run --rm -it -p 3000:80 -p 2525:25 rnwood/smtp4dev
```

**Migrate the database and run the server**
```bash
python3 manage.py migrate
python3 manage.py runserver
```

## API Reference

**Every routes require user to be authenticated. `Authorization: JWT <access_token>` header should be passed in each subsequent request.**


#### Create a user 

```http
  POST /auth/users
```
```json
    {
        "username":"string",
        "email":"string",
        "password":"string"
        "re_password":"string"
    }
```

#### Get the access and refresh token
```http
    POST /auth/jwt/create

```
```json
    {
        "username":"string",
        "password":"string"
    }
```

#### Get all posts 

```http
  GET /api/post/
```

#### Get post

```http
  GET /post/${id}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of post to fetch |

#### POST confession

```http
  POST /api/post/
```

| body | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `title`      | `string` | **Required**. Post title |
| `description`      | `string` | **Required**. Post description |
| `tags`      | `list[string]` | **Required**. Post tags |
| `is_active`      | `boolean` | **Required**. Post active status (Default=True) |


#### GET Comments

```http
  GET /api/post/${id}/comments
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of post to fetch comments |

#### GET Comment

```http
  GET /confess/${id}/comments/${comment_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of post to fetch comments |
| `comment_id`      | `string` | **Required**. Id of comment to fetch |

#### POST Comment

```http
  GET /api/post/${id}/comments/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of confession to fetch replies |

| Body | Type     | Description                            |
| :-------- | :------- | :-------------------------------- |
| `text`      | `string` | **Required**. Comment text to post |
