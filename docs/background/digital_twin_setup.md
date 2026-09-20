# Digital Twin Setup for Autonomous Manufacturing

## Purpose

This document defines the concrete setup for the digital twin used in the autonomous manufacturing system.

It complements `digital_twin.md` by turning the twin concept into a practical configuration that can be implemented, tested, and connected to the agent layer.

## What the Twin Represents

The digital twin models a physical manufacturing asset or subsystem such as:
- conveyor
- pump
- motor
- robotic arm
- packaging unit
- machine cell

The first implementation should model only one asset type so the system stays simple and testable.

## Core Twin Entities

### 1. Asset
Represents the machine or subsystem being modeled.

Fields:
- `asset_id`
- `asset_name`
- `asset_type`
- `location`
- `status`
- `operating_mode`
- `criticality`
- `parent_asset_id`

### 2. Component
Represents a part of the asset.

Fields:
- `component_id`
- `asset_id`
- `component_name`
- `component_type`
- `health_state`
- `wear_level`
- `failure_probability`

### 3. Sensor
Represents a telemetry source attached to the asset.

Fields:
- `sensor_id`
- `asset_id`
- `sensor_type`
- `unit`
- `normal_range`
- `sampling_rate`
- `last_value`
- `last_timestamp`

### 4. Fault Mode
Represents a known failure pattern.

Fields:
- `fault_id`
- `fault_name`
- `symptoms`
- `trigger_conditions`
- `progression_rules`
- `severity`
- `recommended_checks`

### 5. Scenario
Represents a what-if simulation case.

Fields:
- `scenario_id`
- `asset_id`
- `fault_id`
- `input_conditions`
- `candidate_actions`
- `simulation_result`
- `confidence`

## Twin State Model

The twin should maintain a live state object for each asset.

### Suggested state fields
- current status
- active alarms
- recent telemetry window
- detected anomaly flags
- fault hypothesis list
- component health values
- maintenance status
- last simulation result
- confidence score

The state should update continuously as telemetry arrives.

## Telemetry Inputs

The twin should accept read-only telemetry from mock or real sources.

### Input types
- temperature
- vibration
- pressure
- speed
- current draw
- throughput
- alarm codes
- event logs

### Input requirements
- timestamped
- unit-normalized
- source-tracked
- validated for range and type
- stored before being used for simulation

## Operating Limits

Each asset should define limits used by the twin.

### Examples
- max temperature
- max vibration amplitude
- minimum pressure
- acceptable speed range
- max current draw
- alarm severity thresholds

These values are used to detect abnormalities and validate simulation results.

## Failure Modes

Start with a small library of failure modes.

### Suggested initial fault library
- overheating
- bearing wear
- vibration anomaly
- motor slowdown
- pressure drop
- sensor drift
- intermittent fault
- startup failure

### For each fault mode define
- symptom pattern
- expected sensor impact
- severity progression
- likely root causes
- validation logic

## Simulation Setup

The simulation engine should support simple what-if scenarios.

### Scenario examples
- machine continues operating at current load
- machine is restarted
- worn component is replaced
- alarm is ignored for 30 minutes
- maintenance is performed immediately

### Simulation outputs
- predicted state after scenario
- expected alarm changes
- estimated recovery time
- confidence score
- risk flags

## Validation and Safety Rules

The twin must never control real equipment.

### Safety rules
- read-only only
- no PLC write-back
- no autonomous actuation
- no unsafe maintenance recommendations
- operator approval required for critical actions
- every scenario must be explainable

### Validation checks
- simulation matches telemetry patterns
- predicted fault progression is plausible
- recommended actions obey operating limits
- unsafe interventions are flagged

## Data Storage

The twin setup should separate raw input from live state.

### Recommended logical storage
- raw telemetry store
- asset metadata store
- live twin state store
- fault/scenario store
- simulation history store

## Integration Points

The twin should expose outputs to the agent system.

### Shared outputs
- anomaly summary
- current asset state
- fault hypotheses
- scenario results
- safety flags
- evidence references

### Consumed by
- signal agent
- asset-context agent
- knowledge agent
- root-cause agent
- work-instruction agent

## Minimum Viable Twin

The MVP twin should include:
- one asset
- 3 to 5 sensors
- 3 to 5 fault modes
- one simulation engine
- one validation layer
- one API for agent access

## Setup Checklist

- define asset schema
- define telemetry schema
- define operating limits
- define fault library
- define scenario templates
- implement state updates
- implement simulation output
- connect twin to agents
- test safety guardrails

## Summary

This setup turns the digital twin into a usable system component.

It provides structured asset modeling, telemetry ingestion, failure simulation, and safety validation so the maintenance agents can reason over a realistic and explainable representation of the manufacturing system.
