# Exercise 3: Scaling Flask App on Single Node using ReplicaSets

## Real-Life Use Case: E-Commerce Flash Sale
During a flash sale (like Flipkart's Big Billion Days), traffic can spike from 100 to 10,000 requests/minute.  
A single Pod would crash under the load. Using **ReplicaSets**, Kubernetes can scale to 10–20 identical Pods, distributing traffic evenly. Once the sale ends, it scales back down to save resources.

---

## Objective
- Understand ReplicaSets and Pods
- Deploy a Flask app using a ReplicaSet
- Scale the ReplicaSet and observe pod distribution
- Test pod self-healing by deleting a pod

---

## Key Observations and Learnings
- **Pod Distribution** → Each Pod is an identical clone of the app
- **Resiliency** → If one Pod fails, the ReplicaSet automatically creates a replacement
- **Efficiency** → Add Pods when demand spikes, remove them when it's low
- **Real-World Relevance** → This is exactly how Netflix, YouTube, and Swiggy handle peak traffic

---

## Files in This Exercise

| File | Description |
|---|---|
| `app.py` | Flask application simulating a Flash Sale |
| `Dockerfile` | Containerizes the Flask app using Gunicorn |
| `flashsale-replicaset.yaml` | Kubernetes ReplicaSet + Service definition |

---

## Step 1: Clean Up Previous Minikube State

```bash
minikube stop
minikube delete
```

---

## Step 2: Start Minikube with a Single Node

```bash
minikube start --nodes=1
```

**Expected Output:**
```
😄  minikube v1.34.0 on Ubuntu 24.04 (amd64)
✨  Automatically selected the docker driver
👍  Starting "minikube" primary control-plane node in "minikube" cluster
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

Verify:
```bash
kubectl get nodes
```
```
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   42s   v1.31.0
```

---

## Step 3: Build the Docker Image Inside Minikube

Point Docker daemon to Minikube's internal Docker, then build:

```bash
eval $(minikube docker-env)
docker build -t flask-app .
```

---

## Step 4: Apply the ReplicaSet Configuration

```bash
kubectl apply -f flashsale-replicaset.yaml
```

**Expected Output:**
```
replicaset.apps/flashsale-rs created
service/flashsale-svc created
```

---

## Step 5: Verify Pods Are Running

```bash
kubectl get pods
```

**Expected Output:**
```
NAME                 READY   STATUS    RESTARTS   AGE
flashsale-rs-8gbfp   1/1     Running   0          3m35s
flashsale-rs-f4gsl   1/1     Running   0          3m35s
flashsale-rs-nb5kl   1/1     Running   0          3m35s
```

```bash
kubectl get rs
```

```
NAME           DESIRED   CURRENT   READY   AGE
flashsale-rs   3         3         3       3m
```

---

## Step 6: Scale the ReplicaSet to 5 Replicas

```bash
kubectl scale rs flashsale-rs --replicas=5
```

```
replicaset.apps/flashsale-rs scaled
```

Verify:
```bash
kubectl get pods
```

```
NAME                 READY   STATUS    RESTARTS   AGE
flashsale-rs-4nr6q   1/1     Running   0          7m55s
flashsale-rs-84v7x   1/1     Running   0          7m55s
flashsale-rs-nsmlx   1/1     Running   0          32s
flashsale-rs-rbwr4   1/1     Running   0          7m55s
flashsale-rs-wfbb4   1/1     Running   0          32s
```

---

## Step 7: Delete One Pod and Observe Self-Healing

```bash
kubectl delete pod flashsale-rs-84v7x
```

```
pod "flashsale-rs-84v7x" deleted
```

Immediately check again:
```bash
kubectl get pods
```

A **new pod is automatically created** to maintain the desired count of 5:
```
NAME                 READY   STATUS    RESTARTS   AGE
flashsale-rs-4nr6q   1/1     Running   0          9m19s
flashsale-rs-hqtm7   1/1     Running   0          51s   ← new replacement pod
flashsale-rs-nsmlx   1/1     Running   0          116s
flashsale-rs-rbwr4   1/1     Running   0          9m19s
flashsale-rs-wfbb4   1/1     Running   0          116s
```

---

## Step 8: View Pod Distribution Across Nodes

```bash
kubectl get pods -o wide
```

```
NAME                 READY   STATUS    RESTARTS   AGE     IP            NODE
flashsale-rs-4nr6q   1/1     Running   0          10m     10.244.0.9    minikube
flashsale-rs-hqtm7   1/1     Running   0          109s    10.244.0.12   minikube
flashsale-rs-nsmlx   1/1     Running   0          2m54s   10.244.0.11   minikube
flashsale-rs-rbwr4   1/1     Running   0          10m     10.244.0.7    minikube
flashsale-rs-wfbb4   1/1     Running   0          2m54s   10.244.0.10   minikube
```

All 5 pods run on the single minikube node.

---

## Q&A

**Q1. What is the initial number of replicas in the ReplicaSet?**  
A: **3**

**Q2. How many pods are running after applying the ReplicaSet configuration?**  
A: **3**

**Q3. What happens when you scale the ReplicaSet to 5 replicas?**  
A: Kubernetes creates 2 additional pods to reach the desired count of 5.

**Q4. What happens when you delete one pod?**  
A: Kubernetes automatically creates a new replacement pod to maintain the desired count of 5.

**Q5. How does Kubernetes maintain the desired number of replicas?**  
A: Kubernetes continuously compares the current running pods against the desired count. If there is a discrepancy, it creates or deletes pods to match the desired state.

**Q6. How many nodes are running?**  
A: **1** (single minikube node)

**Q7. Where are the pods running with respect to nodes?**  
A: All 5 pods are scheduled on the single minikube node (`minikube`), each with a unique IP address within the cluster subnet (10.244.0.x).
