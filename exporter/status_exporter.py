#!/usr/bin/env python
import requests
from prometheus_client import start_http_server, Gauge
import time
import base64
import argparse

# Define the metric
g = Gauge('connector_status', 'Connector Status. When Running value is 1, when not running value is 0', ['connector'])

def get_environments(username, password):
    url = "https://api.confluent.cloud/org/v2/environments"

    # Encode the credentials in base64
    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

    # Define request headers
    headers = {
        "Authorization": f"Basic {credentials}"
    }

    # Requests the API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Return the env list
        return {env["display_name"]: env["id"] for env in data["data"]}
    else:
        print(f"Error getting environments: {response.status_code}")

def get_clusters(username, password, environment_id):
    url = f"https://api.confluent.cloud/cmk/v2/clusters?environment={environment_id}"

    # Encode the credentials in base64
    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

    headers = {
        "Authorization": f"Basic {credentials}"
    }

    # Requests the API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Analisa a resposta
        data = response.json()

        # Retorn the cluster list
        return {cluster["spec"]["display_name"]: cluster["id"] for cluster in data["data"]}
    else:
        print(f"Error getting clusters: {response.status_code}")

def get_status(env_id, lkc, username, password):
    url = f"https://api.confluent.cloud/connect/v1/environments/{env_id}/clusters/{lkc}/connectors?expand=status"

    # Encode the credentials in base64
    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
    # Define request headers
    headers = {
        "Authorization": f"Basic {credentials}"
    }

    # Faz a requisição à API
    response = requests.get(url, headers=headers)
    if args.debug:
        print(f"GET {url} with response {response.status_code}")

    if response.status_code == 200:
        data = response.json()

        # Iterate over the connectors
        for connector, info in data.items():
            # Check the status of the connector
            status = info["status"]["connector"]["state"]
            if args.debug:
                print(f"Status={status}")

            # Define the metric
            if status == "RUNNING":
                g.labels(connector=connector).set(1)
                if args.debug:
                    print(f"{lkc}=1")
            else:
                g.labels(connector=connector).set(0)
                if args.debug:
                    print(f"{lkc}=0")
    else:
        print(f"Error when obtaining the status of the connectors: {response.status_code}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Monitors the status of Confluent connectors.')
    parser.add_argument('--env', required=True, help='The name of the environment.')
    parser.add_argument('--username', required=True, help='The username for the Confluent Cloud API.')
    parser.add_argument('--password', required=True, help='The password for the Confluent Cloud API.')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode.')
    parser.add_argument('--port-prometheus', required=False, default=8000, type=int, help='The port to expose the Prometheus metrics. (Defaults to 8000)')
    parser.add_argument('--interval', required=False, type=int, default=60, help='The interval to update metrics. (Defaults to 60)')

    args = parser.parse_args()

    # Start Prometheus HTTP
    start_http_server(args.port_prometheus)

    # Get Environment list
    environments = get_environments(args.username, args.password)
    if args.debug:
        print(f"Environments: {environments}")

    # Checks if the env exists
    if args.env in environments:
        # Get Environment ID
        env_id = environments[args.env]
        if args.debug:
            print(f"Env ID: {env_id}")

        # Get Cluster list
        clusters = get_clusters(args.username, args.password, env_id)
        if args.debug:
            print(f"Cluster: {clusters}")

        # Updates connector status
        while True:
            for lkc in clusters:
                cluster_id = clusters[lkc]
                get_status(env_id, cluster_id, args.username, args.password)
            time.sleep(args.interval)
    else:
        print(f"Environment {args.env} was not found.")
