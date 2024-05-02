# Confluent Kafka Connector Status Exporter

Prometheus exporter for `Kafka Connectors` to have the status of each connector in Confluent Cloud, per env.

## Metrics supported
g = Gauge('connector_status', 'Connector Status. When Running value is 1, when not running value is 0', ['connector'])

- `connector_status` Connector Status. When Running value is 1, when not running value is 0

## Configuration

```sh
usage: status_exporter.py [-h] --env ENV --username USERNAME --password PASSWORD [--debug] --port-prometheus PORT_PROMETHEUS [--interval INTERVAL]

options:
  --env ENV             The name of the environment.
  --username USERNAME   The username for the Confluent Cloud API.
  --password PASSWORD   The password for the Confluent Cloud API.
  --debug               Enable debug mode.
  --port-prometheus PORT_PROMETHEUS
                        The port to expose the Prometheus metrics. (Defaults to 8000)
  --interval INTERVAL   The interval to update metrics. (Defaults to 60)
```

## Usage

### Option A) Python3 + PIP

```sh
pip install -r /exporter/requirements.txt
/exporter/status_exporter.py --env ENV --username USERNAME --password PASSWORD [--debug] --port-prometheus PORT_PROMETHEUS [--interval INTERVAL]
```

### Option B) Docker

```sh
docker run --rm -it -p 8000:8000 ghcr.io/lfventura/confluent-connectors-status-exporter:latest /app/status_exporter.py --env ENV --username USERNAME --password PASSWORD [--debug] --port-prometheus PORT_PROMETHEUS [--interval INTERVAL]
```

## Metrics

```sh
# HELP connector_status Status do conector
# TYPE connector_status gauge
connector_status{connector="xxxxx"} x.x
...
```

## Contribute

Feel free to open an issue or PR if you have suggestions or ideas about what to add.