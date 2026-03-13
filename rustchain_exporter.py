#!/usr/bin/env python3
"""
RustChain Prometheus Exporter
Exposes RustChain node metrics for Grafana monitoring.

Usage:
    pip install prometheus-client flask
    python rustchain_exporter.py

Metrics exposed:
- rustchain_up: Node health status
- rustchain_uptime_seconds: Node uptime
- rustchain_epoch: Current epoch number
- rustchain_slot: Current slot
- rustchain_blocks_per_epoch: Blocks per epoch
- rustchain_enrolled_miners: Number of enrolled miners
- rustchain_epoch_pot: RTC reward for current epoch
- rustchain_total_supply_rtc: Total RTC supply
- rustchain_miner_count: Total number of miners
"""

import time
import requests
from prometheus_client import start_http_server, Gauge, Counter, Info
from flask import Flask, Response

# Configuration
RUSTCHAIN_API = "https://rustchain.org"
PORT = 9090

# Prometheus metrics
rustchain_up = Gauge('rustchain_up', 'Node health status (1=up, 0=down)')
rustchain_uptime_seconds = Gauge('rustchain_uptime_seconds', 'Node uptime in seconds')
rustchain_epoch = Gauge('rustchain_epoch', 'Current epoch number')
rustchain_slot = Gauge('rustchain_slot', 'Current slot within epoch')
rustchain_blocks_per_epoch = Gauge('rustchain_blocks_per_epoch', 'Number of blocks per epoch')
rustchain_enrolled_miners = Gauge('rustchain_enrolled_miners', 'Number of enrolled miners')
rustchain_epoch_pot = Gauge('rustchain_epoch_pot', 'RTC reward for current epoch')
rustchain_total_supply = Gauge('rustchain_total_supply_rtc', 'Total RTC supply')
rustchain_miner_count = Gauge('rustchain_miner_count', 'Total number of miners')
rustchain_last_scrape_errors = Counter('rustchain_last_scrape_errors_total', 'Total scrape errors')

# Node info
rustchain_node_info = Info('rustchain', 'RustChain node information')


def scrape_metrics():
    """Fetch metrics from RustChain node."""
    try:
        # Health endpoint
        health = requests.get(f"{RUSTCHAIN_API}/health", timeout=10).json()
        
        if health.get('ok'):
            rustchain_up.set(1)
            rustchain_uptime_seconds.set(health.get('uptime_s', 0))
            rustchain_node_info.info({
                'version': health.get('version', 'unknown'),
                'db_rw': str(health.get('db_rw', False))
            })
        else:
            rustchain_up.set(0)
            
    except Exception as e:
        rustchain_up.set(0)
        rustchain_last_scrape_errors.inc()
        print(f"Error fetching health: {e}")
    
    try:
        # Epoch endpoint
        epoch = requests.get(f"{RUSTCHAIN_API}/epoch", timeout=10).json()
        
        rustchain_epoch.set(epoch.get('epoch', 0))
        rustchain_slot.set(epoch.get('slot', 0))
        rustchain_blocks_per_epoch.set(epoch.get('blocks_per_epoch', 0))
        rustchain_enrolled_miners.set(epoch.get('enrolled_miners', 0))
        rustchain_epoch_pot.set(epoch.get('epoch_pot', 0))
        rustchain_total_supply.set(epoch.get('total_supply_rtc', 0))
        
    except Exception as e:
        rustchain_last_scrape_errors.inc()
        print(f"Error fetching epoch: {e}")
    
    try:
        # Miners endpoint
        miners = requests.get(f"{RUSTCHAIN_API}/api/miners", timeout=10).json()
        rustchain_miner_count.set(len(miners))
        
    except Exception as e:
        rustchain_last_scrape_errors.inc()
        print(f"Error fetching miners: {e}")


# Flask app for metrics endpoint
app = Flask(__name__)

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint."""
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/health')
def health():
    """Health check endpoint."""
    return {'status': 'ok'}


if __name__ == '__main__':
    # Start Prometheus server
    print(f"Starting RustChain exporter on port {PORT}")
    start_http_server(PORT)
    
    # Initial scrape
    scrape_metrics()
    
    # Scrape every 30 seconds
    while True:
        time.sleep(30)
        scrape_metrics()
