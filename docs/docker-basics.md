# Docker Essentials - Daily Commands

## System Commands
```bash
docker --help                    # Get help with Docker commands
docker info                      # Display system-wide information
docker version                   # Show Docker version information
docker system df                 # Show Docker disk usage
docker system prune              # Remove unused data (containers, networks, images)
```

## Working with Images
```bash
# Building images
docker build -t <image_name> .                # Build image from Dockerfile
docker build -t <image_name> . --no-cache     # Build without cache
docker build -t <image_name>:<tag> .          # Build with specific tag

# Managing images
docker images                     # List local images
docker images -a                  # List all images (including intermediates)
docker rmi <image_name>          # Delete an image
docker rmi $(docker images -q)   # Delete all images
docker image prune               # Remove unused images
docker image prune -a            # Remove all unused images
```

## Container Lifecycle
```bash
# Creating and running containers
docker run <image_name>                           # Create and run container
docker run --name <container_name> <image_name>   # Run with custom name
docker run -d <image_name>                        # Run in background (detached)
docker run -it <image_name>                       # Run interactively
docker run --rm <image_name>                      # Auto-remove when container exits

# Managing running containers
docker start <container_name>     # Start stopped container
docker stop <container_name>      # Stop running container
docker restart <container_name>   # Restart container
docker pause <container_name>     # Pause container
docker unpause <container_name>   # Unpause container
```

## Container Operations
```bash
# Viewing containers
docker ps                        # List running containers
docker ps -a                     # List all containers (running and stopped)
docker ps -q                     # List container IDs only

# Container information
docker inspect <container_name>   # Detailed container information
docker logs <container_name>      # View container logs
docker logs -f <container_name>   # Follow logs in real-time
docker logs --tail 50 <container_name>  # Show last 50 log lines

# Executing commands in containers
docker exec -it <container_name> bash    # Open bash shell in container
docker exec -it <container_name> sh      # Open sh shell in container
docker exec <container_name> <command>   # Execute command in container
```

## Networking & Port Mapping
```bash
# Port mapping
docker run -p <host_port>:<container_port> <image_name>    # Map single port
docker run -p 8080:80 nginx                               # Example: map host 8080 to container 80
docker run -P <image_name>                                 # Map all exposed ports

# Container networking
docker network ls                          # List networks
docker network create <network_name>       # Create network
docker run --network <network_name> <image> # Run container on specific network
```

## Volume Management
```bash
# Volume operations
docker volume ls                           # List volumes
docker volume create <volume_name>         # Create volume
docker volume inspect <volume_name>        # Inspect volume
docker volume rm <volume_name>            # Remove volume

# Mounting volumes
docker run -v <host_path>:<container_path> <image>        # Bind mount
docker run -v <volume_name>:<container_path> <image>      # Named volume
docker run -v $(pwd):/app <image>                         # Mount current directory
```

## Container Cleanup
```bash
# Removing containers
docker rm <container_name>        # Remove stopped container
docker rm -f <container_name>     # Force remove running container
docker rm $(docker ps -aq)       # Remove all stopped containers
docker container prune           # Remove all stopped containers
```

## Docker Hub Operations
```bash
# Authentication
docker login                      # Login to Docker Hub
docker login -u <username>        # Login with username
docker logout                     # Logout from Docker Hub

# Image operations
docker search <image_name>         # Search for images on Docker Hub
docker pull <image_name>          # Pull image from registry
docker pull <image_name>:<tag>    # Pull specific tag
docker push <username>/<image_name>  # Push image to Docker Hub
docker tag <image> <username>/<image>:<tag>  # Tag image for pushing
```

## Resource Monitoring
```bash
docker stats                      # Live stream of container resource usage
docker stats <container_name>     # Stats for specific container
docker top <container_name>       # Display running processes in container
docker port <container_name>      # List port mappings
```

## Common Dockerfile Commands
```dockerfile
FROM <base_image>                 # Set base image
RUN <command>                     # Execute command during build
COPY <src> <dest>                 # Copy files from host to image
ADD <src> <dest>                  # Copy files (with extraction support)
WORKDIR <directory>               # Set working directory
EXPOSE <port>                     # Expose port
ENV <key>=<value>                 # Set environment variable
CMD ["executable","param1","param2"]  # Default command
ENTRYPOINT ["executable"]         # Configure container as executable
LABEL <key>=<value>               # Add metadata
```

## Useful Docker Run Options
```bash
-d, --detach          # Run in background
-it                   # Interactive with TTY
--name <name>         # Assign name to container
-p <host>:<container> # Publish ports
-v <host>:<container> # Mount volume
-e <key>=<value>      # Set environment variable
--rm                  # Remove container when it exits
--restart always      # Restart policy
--memory <limit>      # Memory limit
--cpus <number>       # CPU limit
```