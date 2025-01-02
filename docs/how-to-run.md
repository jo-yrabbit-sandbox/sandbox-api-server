## How to run

### Start containers
```sh
cd <top-level>  # top-level directory containing Dockerfile
docker-compose up

# If you've changed source code
docker compose up --build --force-recreate
```

### Test that it's working correctly
1. Sanity check that api-server is running
Url: http://localhost:5000/api/v1/health
Curl command: `curl -X GET http://localhost:5000/api/v1/health`
```json
{"status":"healthy"}
```

2. Get latest message
Url: http://localhost:5000/api/v1/messages/latest?state=test_state
Curl command: `curl -X GET http://localhost:5000/api/v1/messages/latest?state=test_state`
* If messages have been stored in redis, expect outputs like this
```json
{"message":"{'bot_id': 'test_bot_id', 'state': 'test_state', 'text': 'test_text', 'timestamp': 'test_timestamp'}"}
```
* If no messages have been stored in redis, error is expected because redis database has nothing stored in it at this time
```json
{"error":"Error getting latest message - Failed to get latest 1 messages using key state:test_state:messages"}
```

3. Store a message
* Create `test_message.json` 
```json
{
  "bot_id": "test_bot_id",
  "message": {
    "state": "test_state",
    "text": "test_text",
    "timestamp": "test_timestamp"
  }
}
```
* Pass it to curl command to store it
```sh
curl -0 -v POST http://localhost:5000/api/v1/messages \
  -H "Content-Type: text/json; charset=utf-8" \
  -d @test_message.json
```

### Notes

#### Run locally
Note that .env file may have to be updated so that `REDIS_HOST=localhost`.
The name assigned in `docker-compose.yml` is `redis` but when running locally, we do not use docker-compose.
```sh
cd <top-level>  # top-level directory containing Dockerfile
python -m run
```

#### Run api-server in container (without redis)
```
# Build the image
docker build -t api-server .

# Run container
docker run -d \
  -p 5000:5000 \
  --env-file .env \
  --name api-server \
  api-server

# Troubleshooting
docker ps  # Is your container running?
docker ps -a  # Is your container stopped?
docker logs api-server  # Look at logs to see why container stopped

# Teardown
docker stop api-server
docker rm api-server
```