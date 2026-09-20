# GCP Plan for Autonomous Manufacturing Digital Twin

## Objective

This document outlines how to use Google Cloud Platform to build and operate the autonomous manufacturing digital twin described in `digital_twin.md`.

The GCP approach should support:
- read-only industrial data ingestion
- synthetic telemetry for development and testing
- asset state synchronization
- simulation and what-if analysis
- evidence-based maintenance support
- operator-in-the-loop safety controls

## Target GCP Architecture

### 1. Data Ingestion Layer
Use Google Cloud services to ingest telemetry and operational events from mock or read-only sources.

Recommended services:
- **Pub/Sub** for telemetry and alarm streaming
- **Dataflow** for real-time transformation and enrichment
- **Cloud Storage** for raw logs, manuals, and structured exports
- **Cloud Run jobs** or scheduled jobs for batch ingestion

### 2. Storage Layer
Separate raw, curated, and operational data.

Recommended services:
- **Cloud Storage** for raw sensor feeds, manuals, and log archives
- **BigQuery** for analytics, telemetry history, and scenario analysis
- **Firestore** or **Cloud SQL** for live digital twin state and asset metadata

### 3. Twin and Simulation Layer
Host the digital twin services and simulation engine.

Recommended services:
- **Cloud Run** for the twin API and lightweight simulation services
- **GKE** if the architecture requires multiple long-running agent services
- **Cloud Functions** for event-driven updates and alerts
- **Vertex AI** for predictive models, classification, and reasoning support

### 4. Analytics and Search Layer
Support retrieval over manuals, work instructions, and maintenance history.

Recommended services:
- **Vertex AI Search** for indexing manuals and operational knowledge
- **BigQuery** for analytical queries and scenario evaluation
- **Vertex AI** for generative assistance, summary generation, and maintenance reasoning

### 5. Visualization Layer
Provide dashboards and operator views.

Recommended services:
- **Looker** for operational analytics and reporting
- **Cloud Run** or **Firebase Hosting** for a custom front end
- **Google Maps Platform** only if facility or site mapping is needed

## Reference Flow

1. Sensors or mock telemetry publish events to Pub/Sub.
2. Dataflow normalizes and enriches the streams.
3. Raw and curated data are stored in Cloud Storage and BigQuery.
4. Twin state is updated in Firestore or Cloud SQL.
5. Simulation jobs run in Cloud Run, GKE, or Cloud Functions.
6. Vertex AI Search indexes manuals and maintenance records.
7. Vertex AI helps generate hypotheses and work instructions.
8. Looker or a custom app presents current state, predictions, and recommendations.

## Digital Twin Mapping on GCP

### Asset model
Store asset hierarchy and configuration in Cloud SQL or Firestore.

### State model
Store live twin state in Firestore for low-latency document updates.

### Telemetry model
Store raw and historical timeseries in BigQuery and Cloud Storage.

### Failure model
Implement rule-based failure logic in Cloud Run or GKE services, with optional ML models in Vertex AI.

### Decision support
Use Vertex AI plus retrieval from Vertex AI Search to produce ranked hypotheses and safe instructions.

## Security and Safety

GCP should be configured for a read-only OT posture:
- isolate network access using **VPCs** and **Private Service Connect**
- use **service accounts** and least privilege
- restrict telemetry connectors to read-only scopes
- protect secrets with **Secret Manager**
- ensure operator approval is required before recommendations are acted on

## Dev/Test Strategy

For early development:
- simulate telemetry with Cloud Run jobs or local generators
- use mock industrial payloads instead of live plant connections
- deploy the twin in Cloud Run or GKE
- index sample manuals and logs in Vertex AI Search
- validate scenarios using labeled failure cases

## MVP on GCP

A practical first version could include:
- one asset type
- synthetic telemetry ingestion via Pub/Sub
- state storage in Firestore
- a simulation API in Cloud Run
- manual/document retrieval in Vertex AI Search
- operator dashboard in Looker or a small web app

## Advantages of GCP

- Strong analytics with BigQuery
- Simple serverless deployment with Cloud Run and Functions
- Good support for event-driven data pipelines
- Strong search and AI capabilities through Vertex AI
- Efficient path from streaming data to analysis and agent support

## Risks and Considerations

- Avoid overbuilding with too many managed services too early
- Keep OT connections strictly read-only
- Ensure simulation results are explainable and not treated as control commands
- Use a small MVP before expanding to multiple assets or facilities

## Recommended Next Steps

1. Define the minimum asset schema and telemetry schema.
2. Choose Cloud Run or GKE for the twin services.
3. Set up Pub/Sub and BigQuery for ingestion and storage.
4. Index manuals and maintenance logs in Vertex AI Search.
5. Build a single-asset simulation API.
6. Wire the outputs into the maintenance copilot workflow.
