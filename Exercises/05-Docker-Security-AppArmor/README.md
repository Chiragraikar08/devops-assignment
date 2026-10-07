# Exercise 5: Docker Security with AppArmor

## Objective
Understand how to secure Docker containers using **AppArmor profiles** with Python for enforcement.  
Learn how to apply AppArmor profiles using the Docker SDK for Python and test restricted actions within the container.

---

## Scenario
You are deploying a Python Flask application inside Docker. You need to secure it to:
- Restrict access to sensitive directories (`/etc/`, `/var/`)
- Prevent unauthorized binary execution (`/bin/bash`, `/usr/bin/`)
- Limit system capabilities (deny `sys_admin`)

---

## Files in This Exercise

| File | Description |
|---|---|
| `app.py` | Simple secure Flask application |
| `Dockerfile` | Containerizes the Flask app |
| `my-apparmor-profile` | AppArmor security profile (Linux only) |
| `apply_apparmor.py` | Python script using Docker SDK to apply the profile |
| `test_restricted_actions.py` | Python script to test that restrictions work |

---

## Pre-requisites

> ⚠️ **AppArmor requires Linux.** On Windows, you can build the image and run the container, but AppArmor enforcement only works inside Linux / WSL2.

Install AppArmor utilities on Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install apparmor-utils
```

Install Docker SDK for Python:
```bash
pip install docker
```

---

## Task 1: Build the Docker Image

```bash
docker build -t flask-apparmor .
```

**Expected Output:**
```
Sending build context to Docker daemon  3.072kB
Step 1/5 : FROM python:3.8-slim
...
Successfully built flask-apparmor
```

---

## Task 2: Load the AppArmor Profile (Linux Only)

Save the profile to the AppArmor directory:
```bash
sudo cp my-apparmor-profile /etc/apparmor.d/my-apparmor-profile
```

Load it:
```bash
sudo apparmor_parser -r /etc/apparmor.d/my-apparmor-profile
```

---

## Task 3: Run the Container with the AppArmor Profile

```bash
docker run --security-opt="apparmor=my-apparmor-profile" -p 5000:5000 flask-apparmor
```

---

## Task 4: Apply via Docker SDK (apply_apparmor.py)

```bash
python apply_apparmor.py
```

**Expected Output:**
```
Container started: f8c2a7f9b9b8
AppArmor profile applied: ['apparmor=my-apparmor-profile']
```

---

## Task 5: Test Restricted Actions (test_restricted_actions.py)

```bash
python test_restricted_actions.py
```

**Expected Output:**
```
Attempt to read /etc/passwd: Exit Code 1, Output: 
Attempt to execute /bin/bash: Exit Code 126, Output: 
Container stopped
```

The non-zero exit codes confirm that AppArmor **blocked** these restricted actions successfully.

---

## Q&A

**Q1. What is the purpose of using AppArmor with Docker containers?**  
A: AppArmor enforces security policies that confine containerized applications to a limited set of resources. It adds an extra layer of security beyond Docker's default isolation.

**Q2. How do AppArmor profiles help secure a Docker container?**  
A: Profiles define what the containerized process **can** and **cannot** do — restricting file system access, network usage, binary execution, and system calls.

**Q3. Why is it important to restrict access to sensitive directories such as `/etc/` and `/var/`?**  
A: These directories contain critical system configuration files and sensitive data (passwords, logs, settings). Restricting access prevents the container from leaking or tampering with host system data.

**Q4. What other capabilities can you restrict using AppArmor profiles?**  
A: Network access, port binding, binary execution, writing to specific directories, and system administration capabilities (e.g., `cap_sys_admin`, `cap_net_admin`).

**Q5. How can you verify if an AppArmor profile is successfully applied to a Docker container?**  
A: Inspect the container using:
```bash
docker inspect <container_id>
```
Check `HostConfig.SecurityOpt` — it will show `apparmor=my-apparmor-profile` if applied correctly.
