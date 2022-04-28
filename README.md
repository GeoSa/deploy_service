# Deploy service
## Deployment:

### Build image
docker build -t deploy_service --rm /path/to/Dockerfile

### Run container
docker run -dp 8081:5000 --name deploy_Service deploy_service

### Working containers list
docker ps

### Restart container
docker restart deploy_service

### Kill container
docker kill deploy_service

### Delete container
docker rm deploy_service
