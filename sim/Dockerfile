# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the simulator script into the container
COPY cleverhub_sim.py .

# Install any required dependencies
# RUN pip install <dependencies>

# Command to run the simulator with arguments passed via docker-compose
CMD ["python", "cleverhub_sim.py", "server", "12345", "user", "pass", "home"]
