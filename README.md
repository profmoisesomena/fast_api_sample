# FastAPI PostgreSQL Integration Sample

This project demonstrates how to integrate FastAPI with a PostgreSQL database.

## Setup Instructions

1. Make sure you have PostgreSQL installed and running on your machine.

2. Create a database named `fastapi_db`:
   ```
   CREATE DATABASE fastapi_db;
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure your database connection in the `.env` file:
   ```
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=your_db_port
   DB_NAME=fastapi_db
   ```

5. Run the application:
   ```
   uvicorn main:app --reload
   ```

## API Endpoints

- `GET /`: Returns a simple "Esta é uma API de exemplo com FastAPI e PostgreSQL" message.
- `GET /items`: Lists all items from the database.
- `GET /items/{item_id}`: Retrieves an item by its ID from the database.
- `PUT /items/{item_id}`: Creates or updates an item in the database.
- `DELETE /items/{item_id}`: Deletes an item from the database.

## Example Usage Swagger UI

http://localhost:8000/docs

## Other examples and explanations

### List all items
```
GET /items
```

### Get a specific item
```
GET /items/1
```

### Create or update an item
Send a PUT request to `/items/{item_id}` with the following JSON body:

```json
{
  "name": "Example Item",
  "price": 25.99,
  "is_offer": true
}
```

Example using curl:
```
curl -X PUT "http://localhost:8000/items/1" \
     -H "Content-Type: application/json" \
     -d '{"name": "Example Item", "price": 25.99, "is_offer": true}'
```

### Delete an item
```
DELETE /items/1
# fast_api_sample
