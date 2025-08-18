# Docker Troubleshooting Guide

## Quick Debugging Commands
```bash
docker info                       # System information and status
docker system events             # Real-time events from Docker daemon
docker logs <container> --details # Container logs with extra details
docker inspect <container>       # Detailed container information
docker exec -it <container> sh   # Debug inside running container
docker system df                 # Docker disk usage
docker system prune              # Clean up unused resources
```

## Common Container Issues

### 1. Container Won't Start
**Symptoms:** Container exits immediately or fails to start

```bash
# Investigate
docker logs <container_name>      # Check container logs
docker events                    # Monitor Docker events
docker inspect <container_name>   # Check container configuration

# Common causes:
# - Application crashes on startup
# - Wrong CMD/ENTRYPOINT
# - Missing dependencies
# - Port already in use
# - Insufficient permissions
```

**Example debugging:**
```bash
# Test if image works interactively
docker run -it <image_name> sh

# Check if port is already in use
netstat -tulpn | grep <port>
lsof -i :<port>
```

### 2. Container Exits with Code 125/126/127
**Code 125:** Docker daemon error  
**Code 126:** Container command not executable  
**Code 127:** Container command not found  

```bash
# Check container configuration
docker inspect <container_name>

# Test command manually
docker run -it <image_name> sh
# Then run your command manually inside container
```

### 3. "Permission Denied" Errors
```bash
# Check file permissions
docker exec -it <container> ls -la /path/to/file

# Fix permission issues
docker run --user $(id -u):$(id -g) <image>  # Run as current user
docker run --privileged <image>              # Run with elevated privileges (security risk)

# Fix Docker socket permissions (Linux)
sudo usermod -aG docker $USER                # Add user to docker group
sudo systemctl restart docker                # Restart Docker daemon
```

### 4. "Port Already in Use" Error
```bash
# Check what's using the port
sudo netstat -tulpn | grep <port>
sudo lsof -i :<port>

# Kill process using port
sudo kill -9 <PID>

# Use different port
docker run -p 8081:80 <image>  # Instead of 8080:80
```

## Image Build Issues

### 1. Dockerfile Build Failures
```bash
# Build with verbose output
docker build -t <image> . --progress=plain --no-cache

# Debug step by step
docker build -t <image> . --target <stage>   # Multi-stage builds

# Check available space
df -h
docker system df
```

**Common Dockerfile fixes:**
```dockerfile
# Fix: Package installation fails
RUN apt-get update && apt-get install -y <package> && rm -rf /var/lib/apt/lists/*

# Fix: File not found during COPY
COPY --chown=user:group source dest

# Fix: Permission issues
RUN chmod +x /app/script.sh

# Fix: Working directory issues
WORKDIR /app
COPY . .
```

### 2. "No Space Left on Device"
```bash
# Check disk usage
df -h
docker system df

# Clean up Docker resources
docker system prune -f           # Remove unused data
docker image prune -a            # Remove all unused images
docker volume prune              # Remove unused volumes
docker builder prune             # Remove build cache

# Clean up specific resources
docker container prune           # Remove stopped containers
docker rmi $(docker images -f "dangling=true" -q)  # Remove dangling images
```

### 3. Image Pull Issues
```bash
# Network connectivity test
docker run --rm alpine ping -c 3 google.com

# DNS issues
docker run --rm alpine nslookup docker.io

# Registry authentication
docker login                    # Re-authenticate
docker logout && docker login   # Fresh login

# Use different registry mirror
docker pull mirror.gcr.io/library/alpine  # Example alternative
```

## Container Networking Issues

### 1. Container Can't Connect to Other Containers
```bash
# Check networks
docker network ls
docker network inspect bridge

# Test container connectivity
docker exec -it <container1> ping <container2>
docker exec -it <container1> nslookup <container2>

# Create custom network
docker network create mynetwork
docker run --network mynetwork --name app1 <image1>
docker run --network mynetwork --name app2 <image2>
```

### 2. Can't Access Container from Host
```bash
# Check port mapping
docker port <container_name>
docker inspect <container_name> | grep -A 20 "NetworkSettings"

# Test connectivity
telnet localhost <port>
curl http://localhost:<port>

# Check firewall (Linux)
sudo ufw status
sudo iptables -L
```

### 3. DNS Resolution Issues
```bash
# Test DNS inside container
docker exec -it <container> nslookup google.com
docker exec -it <container> cat /etc/resolv.conf

# Set custom DNS
docker run --dns 8.8.8.8 <image>
docker run --dns 1.1.1.1 <image>
```

## Performance Issues

### 1. Container Running Slowly
```bash
# Check resource usage
docker stats <container_name>
docker exec -it <container> top
docker exec -it <container> ps aux

# Check resource limits
docker inspect <container> | grep -A 10 "Resources"

# Monitor system resources
htop
iotop  # For disk I/O
```

### 2. High Memory Usage
```bash
# Set memory limits
docker run -m 512m <image>      # Limit to 512MB
docker run --oom-kill-disable <image>  # Disable OOM killer

# Monitor memory usage
docker stats --no-stream
```

### 3. High CPU Usage
```bash
# Set CPU limits
docker run --cpus="1.5" <image>        # Limit to 1.5 CPUs
docker run --cpu-shares=512 <image>    # Relative CPU weight
```

## Volume and Storage Issues

### 1. Volume Mount Issues
```bash
# Check volume mounts
docker inspect <container> | grep -A 20 "Mounts"

# Test volume accessibility
docker exec -it <container> ls -la /mounted/path
docker exec -it <container> touch /mounted/path/test.txt

# Fix permission issues
docker run -v /host/path:/container/path --user $(id -u):$(id -g) <image>
```

### 2. Data Persistence Issues
```bash
# Create named volume
docker volume create mydata
docker run -v mydata:/data <image>

# Check volume location
docker volume inspect mydata
```

## Docker Daemon Issues

### 1. Docker Daemon Not Running
```bash
# Check daemon status
sudo systemctl status docker
sudo service docker status

# Start Docker daemon
sudo systemctl start docker
sudo service docker start

# Enable Docker on boot
sudo systemctl enable docker
```

### 2. Docker Command Hangs
```bash
# Check daemon logs
sudo journalctl -u docker.service
sudo cat /var/log/docker.log

# Restart Docker daemon
sudo systemctl restart docker
```

## Cleanup and Maintenance

### 1. Regular Cleanup Commands
```bash
# Complete cleanup (use with caution)
docker system prune -a --volumes

# Selective cleanup
docker container prune -f        # Remove stopped containers
docker image prune -f           # Remove unused images
docker volume prune -f          # Remove unused volumes
docker network prune -f         # Remove unused networks

# Remove containers older than 24 hours
docker container prune --filter "until=24h"
```

### 2. Force Remove Stuck Resources
```bash
# Force remove container
docker rm -f <container_name>

# Force remove image
docker rmi -f <image_name>

# Kill all running containers
docker kill $(docker ps -q)

# Remove all containers
docker rm -f $(docker ps -aq)
```

## Debugging Workflow
1. **Check container status**: `docker ps -a`
2. **Examine logs**: `docker logs <container>`
3. **Inspect configuration**: `docker inspect <container>`
4. **Test interactively**: `docker exec -it <container> sh`
5. **Check resource usage**: `docker stats`
6. **Monitor events**: `docker events`
7. **Clean up if needed**: `docker system prune`

## Emergency Commands
```bash
# Stop all containers
docker stop $(docker ps -q)

# Remove everything (DANGER!)
docker system prune -a --volumes --force

# Reset Docker to clean state (DANGER!)
sudo systemctl stop docker
sudo rm -rf /var/lib/docker
sudo systemctl start docker
```