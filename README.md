# Notes

- Send a `PATCH` request to `/fake-data` to generate sample data. Passwords are set equal to usernames.
- Send a `POST` request to `/login` with username/password to receive token
- Tokens are required to
  - `POST`, `PUT`, and `DELETE` at `/posts`
  - `PUT` and `DELETE` at `/users`
- There is no longer `/users/<int:user_id>` for `PUT` and `DELETE`; the relevent `id` is exracted from the token.
- `GET` requests to `/posts` are paginated, accepting `page` and `per_page` parameters