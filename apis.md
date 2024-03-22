# API Endpoint Guide

## User Registration

- **Endpoint:** `/register/`
- **Method:** POST
- **Input:**
  - `username`
  - `password`
- **Output:**
  - JsonFormat:

    ```json
    {
        "message": "Successfully registered."
    }
    ```

## Authentication Token

- **Endpoint:** `/api/token/`
- **Method:** POST
- **Input:**
  - `username`
  - `password`
- **Output:**
  - JsonFormat:

    ```json
    {
        "access_token": "<access token>",
        "refresh_token": "<refresh token>"
    }
    ```

## Token Refresh

- **Endpoint:** `/api/token/refresh/`
- **Method:** POST
- **Input:**
  - **Header:**
    - `Authorization`: `Bearer <refresh token>`
- **Output:**
  - JsonFormat:

    ```json
    {
        "access_token": "<new access token>"
    }
    ```

## Retrieve All Posts

- **Endpoint:** `/blog/posts/`
- **Method:** GET
- **Input:**
  - **Header:**
    - `Authorization`: `Bearer <jwt token>`
- **Output:**
  - JsonFormat: All posts

## Create a New Post

- **Endpoint:** `/blog/posts/`
- **Method:** POST
- **Input:**
  - `title`
  - `content`
  - **Header:**
    - `Authorization`: `Bearer <jwt token>`
- **Output:**
  - JsonFormat:

    ```json
    {
       "id": "<auto generated>",
       "title": "<title you inserted>",
       "content": "<content you inserted>",
       "created_at": "<time that the post created>",
       "updated_at": "<time that the post created>"
    }
    ```

## Update an Existing Post

- **Endpoint:** `/blog/posts/<id>`
- **Method:** PUT
- **Input:**
  - `title`
  - `content`
  - **Header:**
    - `Authorization`: `Bearer <jwt token>`
- **Output:**
  - JsonFormat:

    ```json
    {
       "id": "<id>",
       "title": "<title you inserted>",
       "content": "<content you inserted>",
       "created_at": "<time that the post created>",
       "updated_at": "<time that the post updated>"
    }
    ```

## Retrieve a Specific Post

- **Endpoint:** `/blog/posts/<id>`
- **Method:** GET
- **Input:**
  - **Header:**
    - `Authorization`: `Bearer <jwt token>`
- **Output:**
  - JsonFormat: The post with the specified id.

## Retrieve All Comments

- **Endpoint:** `/blog/comments/`
- **Method:** GET
- **Input:**
  - **Header:**
    - `Authorization`: `Bearer <jwt token>`
- **Output:**
  - JsonFormat: All comments

## Retrieve a Specific Comment

- **Endpoint:** `/blog/comments/<id>`
- **Method:** GET
- **Input:**
  - **Header:**
    - `Authorization`: `Bearer <jwt token>`
- **Output:**
  - JsonFormat: The comment with the specified id.

## Update a Specific Comment

- **Endpoint:** `/blog/comments/<id>`
- **Method:** PUT
- **Input:**
  - `email`
  - `text`
  - `post_id`
  - **Header:**
    - `Authorization`: `Bearer <jwt token>`
- **Output:**
  - JsonFormat:

    ```json
    {
      "id": "<id>",
      "post": "<id of the post>",
      "text": "<text you inserted>",
      "email": "<email you inserted>"
    }
    ```
