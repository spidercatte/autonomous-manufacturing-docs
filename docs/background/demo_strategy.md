# Demo Strategy for Autonomous Manufacturing

## Purpose

This document defines how to demo the autonomous manufacturing system in a way that clearly shows the value of the multi-agent copilot and digital twin.

The demo should emphasize:
- anomaly detection
- asset context retrieval
- root-cause reasoning
- simulation-based validation
- safe maintenance guidance
- operator-in-the-loop decision making

## Demo Goal

The demo should show how the system can take a manufacturing fault from raw telemetry to a safe maintenance recommendation.

## Demo Storyline

### Scenario
A machine or subsystem begins to show abnormal telemetry, such as rising temperature, increased vibration, or a throughput drop.

### Expected flow
1. Synthetic telemetry enters the system.
2. The signal agent detects the anomaly.
3. The asset-context agent retrieves the machine configuration and maintenance history.
4. The knowledge agent retrieves relevant manuals and procedures.
5. The digital twin simulates likely failure progression.
6. The root-cause agent ranks the most likely explanations.
7. The work-instruction agent produces a safe maintenance brief.
8. The operator reviews the recommendation.

## Demo Assets

The demo should use a small, controlled set of sample data:
- one asset hierarchy
- a few sensors
- a few fault scenarios
- mock manuals
- mock maintenance logs
- parts catalog entries
- synthetic time-series telemetry

## Suggested Demo Scenario

### Option 1: Overheating motor
- temperature rises steadily
- vibration gradually increases
- system predicts bearing wear or cooling issue
- twin simulates failure progression
- agent recommends inspection and safe shutdown steps

### Option 2: Conveyor slowdown
- speed drops below normal
- current draw changes unexpectedly
- system checks for motor strain or mechanical blockage
- twin validates maintenance options
- agent generates operator guidance

### Option 3: Sensor drift
- sensor values become inconsistent
- model distinguishes actual fault from false alarm
- twin and knowledge agent cross-check evidence
- system recommends verification steps

## Visuals to Show

The demo UI should show:
- live telemetry chart
- anomaly alert
- asset context panel
- retrieved manual snippets
- twin simulation result
- ranked root-cause list
- maintenance instructions
- safety warnings

## Data Flow in the Demo

1. Synthetic telemetry is published.
2. Ingestion captures the data.
3. The twin updates asset state.
4. Retrieval pulls context and manuals.
5. Agents reason over the evidence.
6. Simulation validates the likely fault.
7. The system outputs a safe recommendation.

## Demo Constraints

- no real PLC write-back
- no autonomous actuation
- no unsafe instructions
- no dependence on live plant data
- all actions remain read-only and explainable

## Success Criteria

The demo is successful if:
- the anomaly is detected
- the root cause is explained with evidence
- the twin simulation matches the scenario
- the work-instruction output is clear and safe
- the operator can understand why the recommendation was made

## Fallback Plan

If live simulation or streaming is unavailable:
- use prerecorded synthetic telemetry
- use static manual excerpts
- replay known failure scenarios
- show the twin state and reasoning outputs from saved data

## Demo Checklist

- telemetry feed ready
- asset and fault data loaded
- manuals indexed
- twin service running
- agents connected
- UI dashboards ready
- fallback dataset prepared
- safety review complete

## Summary

The demo should tell a simple story:

**telemetry anomaly -> evidence gathering -> twin simulation -> root-cause ranking -> safe maintenance guidance**

That sequence will clearly show the value of the autonomous manufacturing system.
