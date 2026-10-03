# Exercise 6: Real-Time Operations Monitoring and Alerting with Grafana

## Objective
You are a DevOps engineer at **ZAPPTTO**, managing a fast-paced delivery service that needs real-time insights.  
Using **Python**, **Prometheus**, and **Grafana**, create a pipeline that:
- Simulates delivery metrics
- Visualizes them on dashboards
- Sets up automated alerts for anomalies

---

## Scenario
Build a monitoring stack that tracks:
- **Total Deliveries**
- **Pending Deliveries**
- **On-the-Way Deliveries**
- **Average Delivery Time**

Alerts fire when pending deliveries exceed 10, or average delivery time exceeds 30 seconds.

---

## Files in This Exercise

| File | Description |
|---|---|
| `delivery_metrics.py` | Python script that simulates and exposes Prometheus metrics |
| `prometheus.yml` | Prometheus scrape configuration |
| `alert_rules.yml` | Alerting rules for Prometheus |
| `Dockerfile` | Containerizes the metrics application |
| `Jenkinsfile` | Jenkins CI pipeline to automate the full stack |

---

## Prerequisites

Install the Prometheus Python client:
```bash
pip3 install prometheus-client
```

---

## Step 1: Run the Python Metrics Application

```bash
python3 delivery_metrics.py
```

**Expected Output:**
```
[INFO] Starting the HTTP server on port 8000...
[INFO] HTTP server started. Simulating deliveries...
[DEBUG] Total deliveries: 69
[DEBUG] Pending deliveries: 20
[DEBUG] On-the-way deliveries: 17
[DEBUG] Average delivery time: 28.26 seconds
[INFO] Sleeping for 1 seconds...
```

Verify metrics are exposed:
```bash
curl http://localhost:8000/metrics
```

You will see raw Prometheus metrics like `total_deliveries`, `pending_deliveries`, etc.

---

## Step 2: Run Prometheus

```bash
docker run -d --name prometheus --network=host \
  -v ./prometheus.yml:/etc/prometheus/prometheus.yml \
  -v ./alert_rules.yml:/etc/prometheus/alert_rules.yml \
  prom/prometheus
```

Access Prometheus at: **http://localhost:9090**

Verify targets are being scraped:  
Go to **Status → Targets** in the Prometheus UI.

---

## Step 3: Run Grafana

```bash
docker run -d --name grafana -p 3000:3000 grafana/grafana
```

Access Grafana at: **http://localhost:3000**  
Login: `admin` / `admin`

---

## Step 4: Configure Grafana

1. Go to **Home → Connections → Data Sources → Add Prometheus**
2. Set URL to: `http://172.17.0.1:9090` (Docker bridge IP)
3. Click **Save & Test**

---

## Step 5: Create Dashboard Panels

Create a new dashboard with 4 panels:

| Panel | Prometheus Query |
|---|---|
| Total Deliveries | `total_deliveries` |
| Pending Deliveries | `pending_deliveries` |
| On-the-Way Deliveries | `on_the_way_deliveries` |
| Avg Delivery Time | `average_delivery_time_sum / average_delivery_time_count` |

---

## Step 6: Run the Jenkins CI Pipeline

Start Jenkins:
```bash
docker run -d -p 8080:8080 -p 50000:50000 \
  --name jenkins \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

Get initial password:
```bash
docker exec -it jenkins bash -c "cat /var/jenkins_home/secrets/initialAdminPassword"
```

Access Jenkins at: **http://localhost:8080**  
Create a **Pipeline job** and paste the contents of `Jenkinsfile`.

---

## Step 7: Simulate Alert Conditions

To trigger the `HighPendingDeliveries` alert, change the range in `delivery_metrics.py`:
```python
pending = random.randint(50, 100)  # Exceeds alert threshold of 10
```

Restart the script. Within 15 seconds, the alert will fire in Prometheus → **Alerts** tab.

---

## Expected Outputs

| Component | URL | What to See |
|---|---|---|
| Metrics Endpoint | http://localhost:8000/metrics | Raw Prometheus metrics |
| Prometheus | http://localhost:9090 | Graphs for delivery metrics |
| Grafana | http://localhost:3000 | Dashboard visualizations |
| Jenkins | http://localhost:8080 | Successful pipeline build |
| Prometheus Alerts | http://localhost:9090/alerts | HighPendingDeliveries alert firing |

---

## Q&A

**Q1. What is the role of `prometheus_client` in this exercise?**  
A: The `prometheus_client` library creates a lightweight HTTP server (on port 8000) that exposes metric data in Prometheus format. Prometheus scrapes this endpoint periodically.

**Q2. What is the difference between a `Gauge` and a `Summary` metric type?**  
A:
- **Gauge**: A value that can go up or down (e.g., current pending deliveries)
- **Summary**: Tracks observed values over time, exposing count and sum for calculating averages (e.g., delivery time)

**Q3. What does `--network=host` do when running Prometheus?**  
A: It makes the Prometheus container share the host machine's network stack, allowing it to reach services running directly on the host (like our Python metrics server on port 8000) via `172.17.0.1`.

**Q4. How does Grafana connect to Prometheus?**  
A: Grafana is configured with Prometheus as a **Data Source**. It sends PromQL queries to Prometheus's HTTP API (`/api/v1/query`) and visualizes the results as graphs on dashboards.

**Q5. What triggers the `HighPendingDeliveries` alert?**  
A: The alert rule `pending_deliveries > 10` — if this condition stays true for 15 seconds (`for: 15s`), Prometheus fires the alert with severity `warning`.
