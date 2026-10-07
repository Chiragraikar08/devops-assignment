# Exercise 4: Docker Networking with Multiple Containers

## Objective
Understand Docker networking concepts and configure a multi-container application using a custom bridge network.

---

## Scenario
Build a web application with three containers communicating on the same Docker network:
- **Container 1** → Python Flask web server
- **Container 2** → MySQL database
- **Container 3** → Redis cache

---

## Files in This Exercise

| File | Description |
|---|---|
| `app.py` | Flask REST API with a `/about` endpoint |
| `Dockerfile` | Containerizes the Flask app |
| `requirements.txt` | Python dependencies |

---

## Task 1: Create a Bridge Network

```bash
docker network create --driver bridge my-bridge-net
```

**Output:**
```
87c23b491f5994c74e497f4f4f4f4f4f4f4f4
```

---

## Task 2: Verify the Network

```bash
docker network ls
```

**Output:**
```
NETWORK ID     NAME            DRIVER    SCOPE
87c23b491f59   my-bridge-net   bridge    local
```

---

## Task 3: Inspect the Network

```bash
docker network inspect my-bridge-net
```

**Output:**
```json
[
    {
        "Name": "my-bridge-net",
        "Driver": "bridge",
        "IPAM": {
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        }
    }
]
```

---

## Task 4: Build the Flask Image

```bash
docker build -t flask-api .
```

---

## Task 5: Launch All Containers on the Network

```bash
docker run -d --name mysql --net=my-bridge-net mysql:latest
docker run -d --name redis --net=my-bridge-net redis:latest
docker run -d --name flask --net=my-bridge-net -p 5001:5001 flask-api
```

Verify all containers are running:
```bash
docker ps
```

---

## Task 6: Test Container-to-Container Connectivity

Enter the Flask container and ping other containers by **name** (Docker DNS resolution):

```bash
docker exec -it flask bash
```

Inside the container:
```bash
ping mysql
```

**Output:**
```
PING mysql (172.18.0.2) 56(84) bytes of data.
64 bytes from mysql (172.18.0.2): icmp_seq=1 ttl=64 time=0.078 ms
```

```bash
ping redis
```

**Output:**
```
PING redis (172.18.0.3) 56(84) bytes of data.
64 bytes from redis (172.18.0.3): icmp_seq=1 ttl=64 time=0.078 ms
```

---

## Task 7: Test the Flask API

```bash
curl http://localhost:5001/about
```

**Expected Output:**
```json
{
  "name": "Simple REST API",
  "version": "1.0",
  "description": "This is a simple REST API built with Flask."
}
```

---

## Task 8: Clean Up

```bash
docker stop mysql redis flask && docker rm mysql redis flask
docker network rm my-bridge-net
```

---

## Q&A

**Q1. What is the purpose of the `--net` flag in `docker run`?**  
A: The `--net` flag connects the container to a specific Docker network, enabling it to communicate with other containers on that same network.

**Q2. How do containers communicate with each other on the same network?**  
A: Containers on the same bridge network communicate using their **container names** as hostnames. Docker's embedded DNS server resolves container names to their internal IP addresses automatically.

**Q3. What is the difference between a bridge network and a host network?**  
A:
- **Bridge Network**: Creates an isolated private network for containers. They talk to each other through the bridge (like being in a private room).
- **Host Network**: The container shares the host machine's network stack directly — no isolation (like being in the same open room as the host).

**Q4. How can you expose a container's port to the host machine?**  
A: Use the `-p` flag: `-p <host_port>:<container_port>`. For example, `-p 5001:5001` maps the container's port 5001 to the host's port 5001.
