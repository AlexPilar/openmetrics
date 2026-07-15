# Open Metrics

## Overview

Open Metrics is an open-source financial data platform designed to centralize, standardize and deliver economic and market data for analytical consumption.
Instead of acting as a traditional dashboard, the platform focuses on building a reliable data foundation by integrating multiple public data sources into a modern analytics architecture.
The long-term vision is to provide investors, analysts and developers with high-quality financial data through dashboards, APIs and analytical applications.

---

## Problem

Financial and macroeconomic data is scattered across multiple public providers, each exposing different APIs, file formats and update frequencies.
Most professional platforms that consolidate these datasets are expensive and primarily targeted at institutional (B2B) customers, making them inaccessible for students, individual investors and small businesses.

---

## Solution

Open Metrics integrates multiple open-data sources into a unified analytics platform.
The project standardizes, validates and models public financial datasets, making them ready for analytical consumption.
Future versions will also provide statistical insights, anomaly detection and educational content for beginner investors.

---

## Architecture

The current architecture follows a modern Analytics Engineering workflow.

```
Open Data Sources
        │
        ▼
Python Connectors
        │
        ▼
Raw Layer (JSON)
        │
        ▼
Bronze Layer (Parquet)
        │
        ▼
DuckDB Warehouse
        │
        ▼
dbt (Staging / Marts)
        │
        ▼
Dashboards & Applications
```

The project separates responsibilities between ingestion (Python), storage (DuckDB) and transformations (dbt), following modern Data Engineering and Analytics Engineering practices.

---

## Tech Stack

- Python
- SQL
- DuckDB
- dbt
- Pandas
- Git
- GitHub

**Planned**

- Streamlit
- Docker
- Airflow
- Microsoft Fabric
- Azure
- Machine Learning

---

## Current Features

- SGS (Brazilian Central Bank) connector
- Metadata catalog
- Automated data ingestion
- Bronze data layer
- DuckDB warehouse
- dbt integration
- Staging models

---

## Roadmap

- Market benchmark and product definition
- Integrate additional Brazilian open-data sources
- Implement dimensional modeling
- Build Gold data marts
- Develop dashboards
- Implement data quality tests
- Add anomaly detection and statistical insights
- Build the user interface
- Publish APIs

---

## Project Structure

```text
open-metrics/

├── connectors/
├── data/
├── warehouse/
├── openmetrics_dbt/
├── docs/
├── tests/
└── README.md
```

---

## Getting Started

Coming soon.

---

## Future Improvements

- International data sources
- Cloud storage
- Airflow orchestration
- Real-time data ingestion
- Machine Learning services
- Public REST API

---

## License

MIT License
