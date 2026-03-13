# RustChain Grafana Dashboard

Prometheus exporter + Grafana dashboard for monitoring RustChain nodes.

![Dashboard Preview](preview.png)

## Quick Start

### 1. Run the Exporter

```bash
# Install dependencies
pip install prometheus-client flask requests

# Run the exporter
python rustchain_exporter.py
```

The exporter will start on `http://localhost:9090/metrics`

### 2. Configure Prometheus

Add to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'rustchain'
    static_configs:
      - targets: ['localhost:9090']
```

### 3. Import Grafana Dashboard

1. Open Grafana
2. Go to Dashboards → Import
3. Upload `dashboard.json` or paste the JSON content

## Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `rustchain_up` | Gauge | Node health (1=up, 0=down) |
| `rustchain_uptime_seconds` | Gauge | Node uptime in seconds |
| `rustchain_epoch` | Gauge | Current epoch number |
| `rustchain_slot` | Gauge | Current slot within epoch |
| `rustchain_blocks_per_epoch` | Gauge | Number of blocks per epoch |
| `rustchain_enrolled_miners` | Gauge | Number of enrolled miners |
| `rustchain_epoch_pot` | Gauge | RTC reward for current epoch |
| `rustchain_total_supply_rtc` | Gauge | Total RTC supply |
| `rustchain_miner_count` | Gauge | Total number of miners |

## API Endpoints

- `GET /metrics` - Prometheus metrics
- `GET /health` - Exporter health check

## Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY rustchain_exporter.py .
RUN pip install prometheus-client flask requests
EXPOSE 9090
CMD ["python", "rustchain_exporter.py"]
```

## Files

- `rustchain_exporter.py` - Prometheus exporter
- `dashboard.json` - Grafana dashboard
- `README.md` - This file

## Bounty

This was created for [RustChain Bounty #1609](https://github.com/Scottcjn/rustchain-bounties/issues/1609)
