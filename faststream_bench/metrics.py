import prometheus_client


CPU_USAGE = prometheus_client.Gauge("cpu_usage", "CPU usage")
