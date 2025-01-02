## How to run locally
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
```

## Test that it's working correctly
1. Open Url: http://localhost:5000/api/v1/health
