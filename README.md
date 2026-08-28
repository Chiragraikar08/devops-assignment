\# Kubernetes Exercise 1 - Hello Pod



\## Objective



Deploy an Nginx web application on Kubernetes using Minikube.



\## Technologies



\- Kubernetes

\- Minikube

\- Docker

\- kubectl

\- Nginx



\## Steps



```bash

minikube start --driver=docker



kubectl run hello-k8s --image=nginx --port=80



kubectl get pods



kubectl expose pod hello-k8s --type=NodePort --port=80



minikube service hello-k8s

