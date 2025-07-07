# irlife-docker

This repository contains the code for the Atelier Capteur AG IRLIFE 2024 in Saint Pée sur Nivelle. It sets up a data pipeline for sensor data using Docker and Docker Compose.

## Project Overview

The project demonstrates how to collect data from two sources:
1.  A Python bot (`bot/bot.py`) simulating temperature data.
2.  A Python script (`bot-yocto/script-yocto.py`) reading CO2, humidity, and pressure data from a Yoctopuce sensor.

Data from both sources is transmitted via MQTT to a Telegraf agent, which then stores the data in an InfluxDB time-series database. Grafana is used for visualizing the data.

## Architecture

The data flows through the following components:

1.  **Simulated Temperature Bot (`bot/`)**: A Python script that generates random temperature data and publishes it to an MQTT topic.
2.  **Yoctopuce Sensor Bot (`bot-yocto/`)**: A Python script that reads data from a Yoctopuce CO2 sensor (including humidity and pressure) and publishes it to MQTT topics.
3.  **Mosquitto (MQTT Broker)**: Receives messages from the bots and forwards them to subscribers.
4.  **Telegraf (`telegraf/`)**: Subscribes to the MQTT topics, processes the incoming data, and writes it to InfluxDB.
5.  **InfluxDB (`influxdb/`)**: Stores the time-series data from Telegraf.
6.  **Grafana (`grafana/`)**: Provides a dashboard to visualize the data stored in InfluxDB.

All services are containerized using Docker and managed with Docker Compose.

## Setup and Running

### Prerequisites

*   Docker
*   Docker Compose

### Configuration

Before running the services, you need to set up an InfluxDB token. This token is used by Telegraf and the Yoctopuce bot to authenticate with InfluxDB.

1.  **Create an InfluxDB Token**:
    *   You can typically create a token through the InfluxDB UI or CLI. For this project, a token might already be provisioned if you are using the provided `docker-compose.yml` which sets up InfluxDB.
    *   The Yoctopuce bot (`script-yocto.py`) and Telegraf (`telegraf.conf`) are configured to read this token from an environment variable named `INFLUX_TOKEN`.

2.  **Set the Environment Variable**:
    *   You will need to make the `INFLUX_TOKEN` environment variable available to the `bot-yocto` and `telegraf` services.
    *   One way to do this with Docker Compose is to create a `.env` file in the root directory of this project with the following content:
        ```
        INFLUX_TOKEN=your_influxdb_token_here
        ```
    *   Replace `your_influxdb_token_here` with your actual InfluxDB token. The `docker-compose.yml` file is usually configured to read this `.env` file.

### Running the Services

1.  Clone this repository.
2.  Navigate to the root directory of the project.
3.  If you haven't already, create the `.env` file as described in the "Configuration" section.
4.  Run the services using Docker Compose:
    ```bash
    docker-compose up -d
    ```
    The `-d` flag runs the containers in detached mode.

5.  **Accessing Services**:
    *   **Grafana**: Open your web browser and go to `http://localhost:3000` (or the port configured for Grafana).
    *   **InfluxDB**: The InfluxDB API is typically available on port `8086`.

## Components

*   **`bot/`**: Contains the Python script for the simulated temperature bot and its Dockerfile.
*   **`bot-yocto/`**: Contains the Python script for the Yoctopuce sensor bot, its Dockerfile, and necessary Yoctopuce libraries.
*   **`docker-compose.yml`**: Defines all the services, networks, and volumes for the Dockerized application.
*   **`grafana/`**: Contains Grafana provisioning files (datasources, dashboards) and storage for Grafana's database.
*   **`influxdb/`**: Contains storage for InfluxDB data.
*   **`mosquitto/config/`**: Contains the configuration file for the Mosquitto MQTT broker.
*   **`telegraf/`**: Contains the Telegraf configuration file (`telegraf.conf`).
*   **`scr/`**: Appears to contain source materials and documentation related to the Yoctopuce sensor.

## Troubleshooting

*   Check container logs using `docker-compose logs <service_name>`. For example, `docker-compose logs telegraf`.
*   Ensure the `INFLUX_TOKEN` is correctly set and accessible by the Telegraf and `bot-yocto` containers.
*   Verify network connectivity between containers if data is not flowing as expected. All services are typically on a Docker-managed network.Tool output for `overwrite_file_with_block`:
