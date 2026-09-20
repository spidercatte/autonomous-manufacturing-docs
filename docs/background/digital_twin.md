# Digital Twin Plan for Autonomous Manufacturing

## Purpose

This document defines the plan for adding a digital twin to the autonomous manufacturing system. The twin is intended to support the existing autonomous maintenance copilot by simulating asset behavior, validating candidate interventions, and helping operators understand likely outcomes before any action is recommended.

The digital twin must fit the current system architecture:

- read-only connections to operational technology
- synthetic or simulated telemetry for development and testing
- asset context and maintenance history
- root-cause analysis and work-instruction generation
- safety-first, operator-in-the-loop behavior
- no autonomous actuation or PLC write-back

## Architecture Alignment

The repository README describes an **Autonomous Maintenance Copilot and Real-Time Root-Cause Discovery** workflow with these core agent roles:

- Signal agent
- Asset-context agent
- Knowledge agent
- Root-cause agent
- Work-instruction agent

The digital twin should support those roles rather than replace them. It will act as a simulation and validation layer that:

1. mirrors the current state of a physical asset or line
2. predicts likely behavior under different fault or repair scenarios
3. validates whether a proposed intervention is plausible
4. provides evidence to the root-cause and work-instruction agents
5. remains read-only and safe

## Goals

### Primary goals
- Simulate equipment behavior using live or synthetic telemetry
- Represent asset states, failure modes, and operating limits
- Predict how faults may evolve over time
- Evaluate candidate maintenance actions before recommending them
- Produce explainable outputs tied to asset context and telemetry

### Secondary goals
- Improve diagnosis confidence by comparing observed signals to simulated behavior
- Provide what-if analysis for maintenance and recovery decisions
- Create a reusable simulation layer for multiple assets
- Support demos using mock equipment, manuals, and failure scenarios

## Non-goals

- No closed-loop control
- No direct PLC write-back
- No autonomous execution of maintenance tasks
- No replacement for the operator or maintenance engineer
- No requirement for high-fidelity physics modeling in the first version

## Proposed Twin Concept

The twin should be a **hybrid digital twin**:

- **State model**: tracks current machine or line state
- **Rules model**: encodes operating constraints, alarms, and failure logic
- **Data-driven model**: learns patterns from historical sensor data and failure events
- **Simulation layer**: runs what-if scenarios for candidate interventions

This combination is a practical fit for the repo’s likely demo and portfolio goals.

## System Placement

The digital twin should sit between telemetry ingestion and downstream agent reasoning.

### Suggested flow
1. Telemetry arrives from:
   - synthetic sensor streams
   - mock PLC/alarm payloads
   - historical logs
   - asset configuration records

2. The twin updates current state:
   - machine status
   - component degradation
   - fault progression
   - operational constraints

3. The twin exposes outputs to:
   - signal agent
   - asset-context agent
   - root-cause agent
   - work-instruction agent

4. The copilot uses twin outputs to:
   - rank likely root causes
   - estimate repair impact
   - validate safe next steps
   - present operator-facing guidance

## Functional Requirements

### 1. Asset state representation
The twin must maintain a structured state for each modeled asset:

- asset identifier
- asset type
- current operating state
- component states
- current alarms
- recent telemetry window
- operating limits
- known failure modes
- maintenance status

### 2. Telemetry ingestion
The twin must accept inputs from mock or real read-only sources:

- time-series sensor data
- alarm payloads
- event logs
- maintenance records
- asset metadata
- fault scenario definitions

### 3. State synchronization
The twin must continuously update its internal model from incoming data:

- reconcile sensor values with expected ranges
- detect deviations from baseline behavior
- mark transitions between normal, degraded, and failed states
- retain history for diagnosis and replay

### 4. Scenario simulation
The twin must support what-if scenarios such as:

- bearing wear progression
- motor overheating
- conveyor slowdown
- sensor drift
- intermittent fault recovery
- replacement of a component
- machine restart after maintenance

### 5. Maintenance validation
The twin should evaluate whether a proposed maintenance action is likely to:

- reduce the fault condition
- restore normal operation
- require additional escalation
- violate a safety or operating constraint

### 6. Explanations and evidence
Outputs must be explainable and tied to evidence:

- signal trends
- rule violations
- historical similarity
- known failure patterns
- predicted outcomes of proposed actions

## Data Inputs

The twin should use the same kinds of inputs described in the README.

### Suggested input categories
- synthetic time-series signals
- mock manuals
- maintenance logs
- parts catalog
- asset hierarchy
- operating limits
- known-failure scenarios
- alarm payloads
- operator annotations

### Input quality rules
- treat manuals and logs as read-only knowledge sources
- never overwrite source records
- isolate untrusted text from prompt injection
- validate data before adding it to the model

## Model Layers

### Layer 1: Asset model
Defines the structure of equipment.

Examples:
- machine
- subsystem
- motor
- pump
- conveyor
- sensor
- controller

### Layer 2: State model
Tracks current condition.

Examples:
- running
- idle
- degraded
- alarmed
- stopped
- under maintenance

### Layer 3: Fault model
Captures known failure patterns.

Examples:
- overheating
- vibration anomaly
- pressure loss
- throughput drop
- intermittent sensor fault
- component wear

### Layer 4: Simulation model
Projects future outcomes.

Examples:
- if the machine continues at current load
- if the operator performs a reset
- if the part is replaced
- if maintenance is deferred

### Layer 5: Decision support layer
Produces results for the maintenance copilot.

Examples:
- most likely root cause
- confidence score
- recommended checks
- expected recovery time
- safety flags

## Service Components

The implementation can be organized into these services or modules.

### 1. Twin State Service
Responsible for:
- storing asset state
- managing current status
- updating state from telemetry
- exposing state to other modules

### 2. Telemetry Adapter
Responsible for:
- ingesting synthetic or live read-only feeds
- normalizing timestamps and units
- mapping raw signals to asset features

### 3. Failure Model Service
Responsible for:
- defining fault modes
- mapping symptoms to possible causes
- tracking failure progression

### 4. Simulation Engine
Responsible for:
- running what-if scenarios
- estimating downstream effects
- comparing alternative interventions

### 5. Validation and Safety Layer
Responsible for:
- checking proposed actions against constraints
- flagging unsafe or unsupported recommendations
- ensuring no autonomous actuation is suggested

### 6. Twin API
Responsible for:
- serving state
- running scenario requests
- returning simulation results
- exposing evidence for agents and UI

## Integration with Existing Agents

### Signal agent
Use the twin to:
- compare incoming signals with expected ranges
- identify abnormal trends
- detect whether a signal pattern matches a known degradation path

### Asset-context agent
Use the twin to:
- retrieve component relationships
- inspect operating limits
- map faults to specific asset configurations

### Knowledge agent
Use the twin to:
- cross-check manuals and procedures against simulated fault behavior
- identify whether a suggested action matches the modeled asset condition

### Root-cause agent
Use the twin to:
- test competing hypotheses
- rank likely root causes by simulated consistency
- explain why one hypothesis fits better than another

### Work-instruction agent
Use the twin to:
- estimate the effect of a repair step
- validate that the repair path is consistent with the simulated fault
- support safe, stepwise instructions

## Suggested MVP Scope

Start with a single machine or subsystem rather than a full factory.

### MVP asset examples
- a motor-driven conveyor
- a pump station
- a robotic arm
- a packaging unit

### MVP signals
- temperature
- vibration
- speed
- pressure
- current draw
- alarm state

### MVP scenarios
- overheating
- component wear
- sensor failure
- temporary downtime
- restart after maintenance

### MVP outputs
- current state snapshot
- top 3 likely failure causes
- simulated outcome of one repair action
- safe next-step recommendation

## Example Data Flow

1. Sensor anomaly appears in telemetry
2. Twin updates current machine state
3. Failure model evaluates likely degradation path
4. Simulation engine compares possible interventions
5. Root-cause agent receives ranked hypotheses
6. Work-instruction agent drafts a safe recovery sequence
7. Operator reviews and confirms action

## Safety and Guardrails

The twin must follow the same safety posture described in the README.

- read-only interfaces only
- no PLC write-back
- no autonomous actuation
- no unsafe repair recommendations
- require operator acknowledgment for critical steps
- isolate and sanitize untrusted text sources
- avoid treating manuals as executable instructions

## Validation Strategy

The twin should be validated against known scenarios.

### Validation checks
- Does the simulated fault match expected symptoms?
- Does the twin recover when the modeled repair is applied?
- Are the root-cause rankings consistent with labeled scenarios?
- Are predictions stable across repeated runs?
- Do results remain explainable to an operator?

### Acceptance criteria
- Twin state reflects incoming telemetry correctly
- Simulation outputs change when inputs change
- Repair validation identifies safe vs unsafe actions
- Root-cause ranking improves over baseline heuristics
- Results are useful in a demo setting

## Implementation Phases

### Phase 1: Foundation
- define asset schema
- define state schema
- define telemetry schema
- add read-only data ingestion

### Phase 2: Simulation core
- implement failure modes
- add scenario runner
- produce predicted state transitions

### Phase 3: Agent integration
- connect twin outputs to the maintenance copilot agents
- expose evidence and scenario comparisons

### Phase 4: Validation and refinement
- test against known failure scenarios
- tune fault rules and signal thresholds
- improve explainability

## Deliverables

The digital twin work should produce:

- asset and state schema
- telemetry adapter
- failure model definitions
- simulation engine
- scenario runner
- API or service interface
- example failure scenarios
- operator-facing outputs
- documentation of safety constraints

## Recommended Repository Fit

This plan should correspond to the current repo direction by emphasizing:

- autonomous maintenance
- real-time root-cause discovery
- synthetic or mocked inputs
- industrial safety
- evidence-based recommendations
- digital twin simulation as a stretch capability

## Summary

The digital twin for this system should be a practical, safe, read-only simulation layer that supports the autonomous maintenance copilot. It should help the agents reason about machine state, evaluate fault hypotheses, and validate maintenance actions without ever controlling the real equipment.

The best initial implementation is a narrow twin for one asset type, with structured telemetry, state tracking, simple failure rules, and scenario simulation tied directly into the existing agent workflow.

## Proactive mode (implemented)

The twin above is reactive: an alarm arrives and the copilot diagnoses it. A second trigger is now implemented as a
runnable slice in [`proactive/`](../../proactive/README.md): an external event (for example an extreme-heat forecast) is
analysed against the twin, and the system proposes a scheduled machine adjustment.

The flow is: detect, analyse, recommend, dry run, rollback plan, human review, schedule, pre-execution validation,
**simulated** execution, monitoring, learning. It reuses the twin's state / rules / data-model split and keeps every
constraint in this document: read-only OT, operator in the loop, no PLC write-back. Execution changes the twin's state
only. The dashboard opens on normal plant operation; an external event triggers a recommendation run, which opens into
a simulation view with the dry run, schedule choice, a read-only Twin Assistant chat and the approval controls. See
`../../proactive/README.md` for the demo, the mapping to each step and what is not yet built.
