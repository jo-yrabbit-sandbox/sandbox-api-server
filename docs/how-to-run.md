## How to run

### Start containers
```sh
cd <top-level>  # top-level directory containing Dockerfile
docker-compose up
```

### Test that it's working correctly
1. Open Url: http://localhost:5000/api/v1/health
```json
{"status":"healthy"}
```
2. Make a request: http://localhost:5000/api/v1/messages/latest?state=test
Note that error is expected because redis database has nothing stored in it at this time
```json
{"error":"Error getting latest message - Failed to get latest 1 messages using key state:positive:messages"}
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