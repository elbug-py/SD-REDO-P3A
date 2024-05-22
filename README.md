# How to build

1. Build and run the docker-compose file
```bash
docker-compose up --build
```
2. Access the container
```bash
docker exec -it cleverhub bash
```
3. By default, the container will run the simulator. You have to run the client to interact with the simulator
4. To run more clients, you can run the following command, changing the ALIAS variable as needed
```bash
docker-compose run -e ALIAS=client2 client
```