## How to run locally

### To build and run
```sh
cd <top-level>  # top-level directory containing Dockerfile

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
```

### Test that it's working correctly
1. Open Url: http://localhost:5000/api/v1/health


### Teardown
```sh
docker stop api-server
docker rm api-server
```