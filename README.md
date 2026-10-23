# DevOps Lab Portfolio — Chirag Raikar

> A collection of 10 hands-on DevOps labs covering Kubernetes, Docker, Jenkins CI/CD, and real-time monitoring — completed as part of a structured DevOps engineering program.

---

## 🛠️ Tech Stack

![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat&logo=kubernetes&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=flat&logo=jenkins&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat&logo=grafana&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)

---

## 📋 Labs Overview

| # | Lab | Key Concepts | Tools |
|---|-----|-------------|-------|
| 01 | [Nginx Pod on Kubernetes](#lab-01-nginx-pod-on-kubernetes) | Pod deployment, NodePort Service, kubectl | Minikube, kubectl |
| 02 | [Flask App on Minikube](#lab-02-flask-app-on-minikube) | Deployments, Services, imagePullPolicy | Minikube, kubectl, Docker |
| 03 | [ReplicaSet Scaling](#lab-03-replicaset-scaling) | ReplicaSets, horizontal scaling, self-healing | Minikube, kubectl |
| 04 | [Docker Networking](#lab-04-docker-networking) | Bridge networks, DNS resolution, multi-container | Docker |
| 05 | [Docker Security](#lab-05-docker-security) | AppArmor profiles, Docker SDK, capability restriction | Docker, AppArmor, Python |
| 06 | [Grafana Monitoring](#lab-06-grafana-real-time-monitoring) | Prometheus metrics, Grafana dashboards, alerting | Prometheus, Grafana, Python |
| 07 | [Jenkins Introduction](#lab-07-jenkins--ci-introduction) | CI concepts, Jenkins installation | Jenkins, Docker |
| 08 | [Hello World Jenkins](#lab-08-hello-world-jenkins-job) | Freestyle jobs, SCM integration, shell build steps | Jenkins, GitHub |
| 09 | [Jenkins Multi-Stage Pipeline](#lab-09-jenkins-multi-stage-pipeline) | Declarative pipelines, Build/Test/Deploy stages | Jenkins, Python, Flask |
| 10 | [Kubernetes Multi-Node](#lab-10-kubernetes-multi-node-cluster) | Multi-node clusters, pod anti-affinity, microservices | Minikube, kubectl, Docker |

---

## Lab 01: Nginx Pod on Kubernetes

**Folder:** [`01-Nginx-Pod/`](./01-Nginx-Pod/)

Deployed an Nginx web server as a Kubernetes Pod on Minikube and exposed it using a `NodePort` Service. Verified HTTP access via `kubectl port-forward`.

**Key Steps:**
- Started Minikube and verified cluster health
- Deployed Nginx pod using `kubectl run`
- Exposed pod via NodePort Service
- Accessed Nginx welcome page at `http://localhost:8080`

---

## Lab 02: Flask App on Minikube

**Folder:** [`02-Kubectl-Flask/`](./02-Kubectl-Flask/)

Deployed a Python Flask application on Minikube using YAML manifests. Understood the difference between `port` and `targetPort`, and why a Service is needed for external access.

**Key Steps:**
- Built Flask Docker image inside Minikube's Docker daemon (`eval $(minikube docker-env)`)
- Applied `Deployment` YAML with `imagePullPolicy: Never`
- Added `NodePort` Service to the manifest
- Accessed app via `minikube service flask-app-service --url`

---

## Lab 03: ReplicaSet Scaling

**Folder:** [`03-Minikube-Scaling/`](./03-Minikube-Scaling/)

Deployed a Flash Sale e-commerce simulation app using a Kubernetes ReplicaSet. Scaled from 3 → 5 replicas and observed automatic self-healing when a pod was deleted.

**Key Steps:**
- Started Minikube with `--nodes=1`
- Applied ReplicaSet + Service YAML (3 initial replicas)
- Scaled to 5 replicas with `kubectl scale rs flashsale-rs --replicas=5`
- Deleted a pod and observed automatic replacement

---

## Lab 04: Docker Networking

**Folder:** [`04-Docker-Networking/`](./04-Docker-Networking/)

Created a custom Docker bridge network and connected Flask, MySQL, and Redis containers on it. Verified that containers can communicate using DNS names instead of IP addresses.

**Key Steps:**
- Created bridge network: `docker network create --driver bridge my-bridge-net`
- Launched 3 containers on the same network
- Exec'd into Flask container and pinged mysql/redis by name
- Confirmed DNS-based container-to-container communication

---

## Lab 05: Docker Security

**Folder:** [`05-Docker-Security/`](./05-Docker-Security/)

Secured a Docker container using an AppArmor profile that restricts access to `/etc/`, `/var/`, and binary execution. Used the Docker SDK for Python to apply and verify the profile.

**Key Steps:**
- Wrote `my-apparmor-profile` restricting sensitive paths and capabilities
- Loaded the profile: `sudo apparmor_parser -r ...`
- Ran container with `--security-opt="apparmor=my-apparmor-profile"`
- Verified restrictions using `test_restricted_actions.py` (Exit Code 1/126 for blocked ops)

---

## Lab 06: Grafana Real-Time Monitoring

**Folder:** [`06-Grafana-Monitoring/`](./06-Grafana-Monitoring/)

Built a real-time delivery operations monitoring stack using Python (prometheus_client), Prometheus, and Grafana. Configured alerting rules that fired when pending delivery thresholds were exceeded.

**Key Steps:**
- Wrote `delivery_metrics.py` exposing Gauge and Summary metrics on port 8000
- Ran Prometheus with `prometheus.yml` + `alert_rules.yml` via Docker
- Ran Grafana and connected Prometheus as a data source
- Created dashboard panels for total/pending/on-the-way deliveries and avg delivery time
- Verified `HighPendingDeliveries` and `HighAverageDeliveryTime` alerts firing in Prometheus UI
- `Jenkinsfile` + `Dockerfile` provided for full stack automation via Jenkins

**Monitoring Stack:**

| Service | URL | Purpose |
|---------|-----|---------|
| Metrics Endpoint | `http://localhost:8000/metrics` | Live Prometheus metrics |
| Prometheus UI | `http://localhost:9090` | Queries, targets, alerts |
| Grafana Dashboard | `http://localhost:3000` | Real-time visualizations |

---

## Lab 07: Jenkins & CI Introduction

**Folder:** [`07-Jenkins-Pipeline/`](./07-Jenkins-Pipeline/)

Studied Continuous Integration concepts and installed Jenkins using Docker. Covered key CI features, benefits, common CI/CD tools (GitLab CI, CircleCI, Travis CI, Bamboo, TeamCity, GitHub Actions), and core Jenkins concepts.

**Key Steps:**
- Ran Jenkins via Docker: `docker run -d -p 8080:8080 jenkins/jenkins:lts`
- Retrieved initial admin password and unlocked Jenkins at `http://localhost:8080`
- Installed suggested plugins and created admin user

---

## Lab 08: Hello World Jenkins Job

**Folder:** [`08-HelloWorld-Jenkins/`](./08-HelloWorld-Jenkins/)

Created a Jenkins Freestyle job that pulls a shell script from GitHub and executes it. Demonstrated SCM integration and basic Jenkins job configuration.

**Key Steps:**
- Created GitHub repository and pushed `hello-world.sh`
- Configured Freestyle job with Git SCM and shell build step (`sh hello-world.sh`)
- Built the job and verified "Hello, Jenkins!" in the console output

---

## Lab 09: Jenkins Multi-Stage Pipeline

**Folder:** [`09-Jenkins-MultiStage/`](./09-Jenkins-MultiStage/)

Designed and ran a Jenkins declarative pipeline with 5 stages for a Python Flask application: **Build → Test → Deploy → Run Application → Test Application**. Resolved missing Python dependencies inside the Jenkins container.

**Key Steps:**
- Pushed Flask app, unit tests, and `Jenkinsfile` to GitHub
- Created Jenkins Pipeline job with "Pipeline script from SCM"
- Resolved `python3`/`pip` dependencies inside Jenkins container via `docker exec`
- All 5 stages completed with `Finished: SUCCESS`

---

## Lab 10: Kubernetes Multi-Node Cluster

**Folder:** [`10-Kubernetes-MultiNode/`](./10-Kubernetes-MultiNode/)

Deployed two Flask microservices (Product Catalog and Shopping Cart) on a 3-node Minikube cluster. Used pod anti-affinity rules to ensure pods from the same service are scheduled on different nodes.

**Key Steps:**
- Started 3-node cluster: `minikube start --nodes 3 -p devops-multinode`
- Built and loaded Docker images for both services into Minikube
- Applied Deployments (2 replicas for Catalog, 3 for Cart) with `podAntiAffinity`
- Verified pods spread across `devops-multinode`, `devops-multinode-m02`, `devops-multinode-m03`
- Tested APIs via `curl` — product list and cart add/retrieve working

---

## 📁 Repository Structure

```
devops-assignment/
├── 01-Nginx-Pod/                     # Lab 01: Nginx Pod on Minikube
├── 02-Kubectl-Flask/                 # Lab 02: Flask App deployment via kubectl
├── 03-Minikube-Scaling/              # Lab 03: ReplicaSet scaling & self-healing
├── 04-Docker-Networking/             # Lab 04: Multi-container Docker bridge network
├── 05-Docker-Security/               # Lab 05: AppArmor container security
├── 06-Grafana-Monitoring/            # Lab 06: Prometheus + Grafana monitoring stack
├── 07-Jenkins-Pipeline/              # Lab 07: CI theory + Jenkins installation
├── 08-HelloWorld-Jenkins/            # Lab 08: First Jenkins Freestyle job
├── 09-Jenkins-MultiStage/           # Lab 09: Multi-stage Jenkins pipeline
├── 10-Kubernetes-MultiNode/          # Lab 10: Multi-node K8s with microservices
└── README.md                         # This file
```

---

## 🔧 Environment

| Tool | Version |
|------|---------|
| OS | Windows 11 / WSL2 (Ubuntu) |
| Docker Desktop | Latest |
| Minikube | v1.38.1 |
| Kubernetes | v1.35.1 |
| Python | 3.10+ |
| Jenkins | LTS (Docker image) |
| Prometheus | Latest (Docker image) |
| Grafana | Latest (Docker image) |

---

## 👤 Author

**Chirag Raikar**
- GitHub: [Chiragraikar08](https://github.com/Chiragraikar08)
- Repository: [devops-assignment](https://github.com/Chiragraikar08/devops-assignment)
