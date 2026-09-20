# Whiteboard Input: Aircraft Engine Manufacturing
## Six Sigma Process Variability Copilot & Predictive Maintenance

---

## **1. PROBLEM STATEMENT**

### Current State (Industry Baseline)
Aircraft engine manufacturers (Rolls-Royce, GE Aviation, Pratt & Whitney) face **silent process drift** that cascades to catastrophic component failures:

- **Process Capability (Cpk):** Currently ~1.1 (degrading from 1.6 over 2-3 cycles undetected)
- **Defect Rate (DPMO):** 60,000 per million opportunities (99.4% conformance)
- **Unplanned Downtime:** 27 hours/month per facility
- **Cost Per Downtime Event:** $260K-$2.3M per hour
- **Monthly Downtime Cost:** $7-15M per facility
- **Annual Downtime Exposure:** $84-180M per facility

### The Gap
Automated telemetry sensors (PLC data) trigger error codes **only after failure begins**. Operators lack:
- Real-time statistical process control (SPC) monitoring
- Early detection of increasing variability (σ trending up)
- Correlation between process drift and component wear
- Predictive maintenance windows (parts ordering lead time)
- Six Sigma analytics to prioritize which variability matters most

**Result:** 4-hour average diagnosis time while production stalls.

---

## **2. USE CASE: PROCESS VARIABILITY → EQUIPMENT FAILURE**

### Critical-to-Quality (CTQ) Parameters for Jet Engines

| Parameter | Nominal | USL | LSL | Current Cpk | Target Cpk | Failure Mode if Out-of-Spec |
|-----------|---------|-----|-----|-------------|-----------|------------------------------|
| **Fuel Injection Pressure** | 240 bar | 250 | 230 | 1.2 | 1.67 | Combustor hot spots, cracks |
| **Compressor Discharge Temp** | 150°C | 160 | 140 | 1.1 | 1.67 | Thermal cycling → seal failure |
| **Blade Clearance** | 1.5mm | 1.55 | 1.45 | 1.3 | 1.67 | FOD damage, blade rub |
| **Rotor Balance** | 0.5g | 0.5 | 0g | 1.0 | 1.67 | Vibration → bearing wear |
| **Coating Thickness** | 0.3mm | 0.35 | 0.25 | 1.4 | 1.67 | Accelerated oxidation |

### Failure Cascade Example: Fuel Nozzle Wear

```
Cycle 820:  σ = 6 bar (normal, Cpk = 1.6)
Cycle 825:  σ = 7 bar (slight increase)
Cycle 830:  σ = 9 bar (warning: Cpk = 1.1)  ← EARLY ALERT HERE
Cycle 840:  σ = 12 bar (alarm: Cpk = 0.8)
Cycle 850:  Combustor crack detected (catastrophic failure)
           → 20-hour diagnosis + repair
           → $5-10M cost
           → 5+ day production stoppage
```

**With predictive detection at Cycle 830:**
- Order replacement nozzles (14-day lead time)
- Schedule maintenance during next planned downtime
- **Prevent cascade failure entirely**

---

## **3. SOLUTION ARCHITECTURE**

### Five-Agent Multi-Agent System

#### **Agent 1: Signal Agent (SPC Monitor)**
**Purpose:** Real-time statistical process control

- Monitor incoming sensor streams (10+ parameters)
- Calculate μ (mean) and σ (standard deviation) per cycle
- Compute Cpk in real-time: `Cpk = (USL - μ) / 3σ`
- Flag SPC violations:
  - 8+ consecutive points above center line (process shift)
  - Cpk trending downward (increasing variability)
  - σ increasing >20% over 5 cycles (instability)
- Alert: "Fuel pressure σ increased 40% in last 10 cycles"

#### **Agent 2: Asset-Context Agent (Predictive Wear)**
**Purpose:** Historical component wear lifecycle prediction

- Retrieve asset history:
  - Equipment serial number, age (cycles/hours)
  - Past maintenance actions and outcomes
  - Component service life curves
- Calculate time-to-failure:
  - If fuel nozzle degradation curve shows failure at σ > 12 bar
  - Current trend: σ increasing at +0.2 bar/cycle
  - ETA failure: 15 cycles (approximately 2 months)
- Output: "Schedule fuel nozzle replacement in 2 months (14-day parts lead time required)"

#### **Agent 3: Knowledge Agent (CTQ + FMEA)**
**Purpose:** Parse specifications and prioritize failure risks

- Retrieve CTQ specifications (USL/LSL, tolerance windows)
- Access Failure Mode & Effects Analysis (FMEA) register
- Calculate Risk Priority Numbers (RPN = Severity × Occurrence × Detection)
  - Example: Fuel nozzle pressure drift RPN = 378 (HIGH priority)
- Link sensor parameters to failure modes
- Output: "3 failure modes linked to fuel pressure: Combustor crack (RPN 378), Flame holder recession (RPN 245), Thermal gradient (RPN 189)"

#### **Agent 4: Root-Cause Agent (Pareto Analysis)**
**Purpose:** Rank which variability drivers cause failures (80/20 Rule)

- Historical failure database analysis:
  - Of 150 combustor cracks: 45% from fuel pressure drift, 30% from temp spikes, 15% from rotor imbalance, 10% other
- Current alarm correlation:
  - Pressure σ increasing + temp stable + vibration normal → 85% probability fuel nozzle wear
  - Pressure normal + temp spiking + vibration normal → 70% probability blade fouling
- Output: "Ranked hypotheses: (1) Fuel nozzle wear 85%, (2) Blade fouling 10%, (3) Seal degradation 5%"

#### **Agent 5: Work-Instruction Agent (Preventive Controls)**
**Purpose:** Generate actionable maintenance procedures

**For Fuel Pressure Drift (Cpk < 1.33):**
- Immediate action:
  - Alert operator: "Fuel pressure variability exceeding limits"
  - Check suction-side pressure (cavitation indicator)
  - Perform fuel system flush
  - Verify return pressure and nozzle spray pattern
  
- Preventive maintenance (σ trending up):
  - If σ > 6 bar: Schedule nozzle inspection (cost: $2K, 4 hours)
  - If σ > 8 bar: Replace fuel nozzles (cost: $2K, 8 hours)
  - Lead time: 14 days for parts
  
- Escalation (corrective action fails):
  - Halt engine from production
  - Escalate to engineering for root-cause analysis
  - Potential engine rebuild ($500K+)

---

## **4. INDUSTRY STANDARDS & METRICS**

### Quality Certification Requirements
- **AS9100:** Primary aerospace QMS standard (mandatory compliance)
- **AS9145:** Advanced Product Quality Planning & Production Part Approval
- **NADCAP:** Special process control (coatings, heat treatment, welding)
- **FAA 14 CFR Part 33:** Airworthiness standards for aircraft engines
- **SAE/AIAA Standards:** Industry-wide manufacturing best practices

### Current Industry Benchmarks

| Metric | Industry Target | Best-in-Class | Your Target |
|--------|-----------------|---------------|-------------|
| **First Pass Yield (FPY)** | >95% | 98%+ | 98% |
| **DPMO (Defects Per Million)** | 60-1,000 DPPM | <50 DPPM | <50 DPPM |
| **Process Capability (Cpk)** | ≥1.33 min | 1.67-2.0 | 1.67+ |
| **Tolerance Specification** | ±0.01-0.1mm | ±0.001mm (1 micron) | ±0.001-0.01mm |
| **Unplanned Downtime** | 27 hrs/month | <10 hrs/month | <10 hrs/month |
| **Mean Time to Diagnosis** | 4 hours | 15 minutes | 15 minutes |

---

## **5. SUCCESS METRICS (SIX SIGMA FRAMEWORK)**

### DEFINE Phase
- ✅ Map 5 critical CTQ parameters
- ✅ Define tolerance windows (USL/LSL)
- ✅ Set baseline Cpk (current state: ~1.1-1.3)
- ✅ Target: Cpk >1.67 (world-class for safety-critical)

### MEASURE Phase
- ✅ Collect real-time sensor streams
- ✅ Calculate μ, σ per cycle per parameter
- ✅ Track DPMO trending (goal: reduce 60K → <10K)
- ✅ Establish SPC control charts

### ANALYZE Phase
- ✅ Pareto analysis: Top 3 variability drivers
- ✅ FMEA ranking: Risk priority by failure mode
- ✅ Historical correlation: Which patterns precede failures
- ✅ Cpk degradation detection: Identify when process shifts

### IMPROVE Phase
- ✅ Preventive maintenance triggers (Cpk thresholds)
- ✅ Process adjustment recommendations
- ✅ Component wear curve modeling
- ✅ Lead time-based ordering alerts

### CONTROL Phase
- ✅ Real-time SPC dashboards (control chart rules)
- ✅ Continuous Cpk monitoring
- ✅ Outcome feedback loop (update wear curves)
- ✅ Trending DPMO reduction toward target

### Quantified Impact

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| **Cpk** | 1.1-1.3 | 1.67+ | +35-50% |
| **DPMO** | 60,000 | <10,000 | 83% reduction |
| **Unplanned Downtime/Month** | 27 hours | 10-15 hours | 40-50% reduction |
| **Monthly Downtime Cost** | $7-15M | $3-7.5M | $4-8M savings |
| **Annual Cost Avoidance** | Baseline | $48-108M | **$48-108M per facility** |
| **Mean Time to Diagnosis** | 4 hours | 15 minutes | 16x faster |

---

## **6. MOCK INPUT DATA STRUCTURE**

### A. Sensor Telemetry (Time-Series)
```yaml
engine_sn: "A1234"
cycle: 830
timestamp: "2026-09-11T14:32:00Z"

sensors:
  fuel_pressure:
    current_reading: 238 bar
    mean_last_10_cycles: 241 bar
    sigma_last_10_cycles: 9.2 bar  # (was 6 bar at cycle 820)
    cpk: 1.08  # (was 1.6)
    status: "CAUTION - Cpk degrading"
  
  compressor_discharge_temp:
    current_reading: 155°C
    mean_last_10_cycles: 152°C
    sigma_last_10_cycles: 4.1°C
    cpk: 1.46
    status: "NORMAL"
  
  rotor_balance:
    current_reading: 0.48g
    mean_last_10_cycles: 0.42g
    sigma_last_10_cycles: 0.35g
    cpk: 0.95  # (at risk)
    status: "ALERT - approaching limit"
```

### B. CTQ Specification Database
```yaml
ctq_fuel_pressure:
  nominal: 240 bar
  usl: 250 bar
  lsl: 230 bar
  cpk_target: 1.67
  alert_threshold_sigma: 6 bar
  failure_modes:
    - name: "Combustor hot spot"
      probability_at_cpk_1.2: 0.25
      lead_time_to_failure: "50-100 cycles"
      severity_rpn: 9
    - name: "Flame holder recession"
      probability_at_cpk_1.2: 0.15
      severity_rpn: 8
```

### C. FMEA Register
```yaml
failure_mode_001:
  name: "Combustor crack"
  root_causes:
    - cause: "Fuel nozzle wear"
      occurrence: 7
      detection: 6
      severity: 9
      rpn: 378
    - cause: "Thermal cycling"
      occurrence: 5
      detection: 4
      severity: 9
      rpn: 180
```

### D. Historical Failure Cases (Labeled)
```yaml
case_001:
  engine_sn: "A1234"
  failure_mode: "Combustor crack"
  root_cause: "Fuel nozzle wear"
  detected_cycle: 847
  failed_cycle: 875
  predictable_cycles_in_advance: 28
  
  sensor_patterns:
    fuel_pressure_sigma: 10.5  # (escalating)
    fuel_pressure_mean: 235    # (drifting low)
    rotor_balance_sigma: 0.5   # (stable)
    temp: "stable"
  
  preventive_action: "Replace fuel nozzles"
  outcome: "Success - 500+ cycles without recurrence"
```

---

## **7. DEMO SCENARIOS**

### Scenario 1: Normal Operation (Cpk Stable)
- All CTQ parameters within control limits
- Cpk > 1.33 for all parameters
- No alerts, no action needed
- **Agent output:** "Engine operating normally. All parameters in green zone."

### Scenario 2: Gradual Wear (Preventive Maintenance Recommended)
- Fuel pressure σ increasing: 6 → 7 → 9 bar (5 cycles)
- Cpk degrading: 1.6 → 1.3 → 1.1
- Match historical pattern: 85% confidence fuel nozzle wear
- **Agent output:** "CAUTION: Fuel pressure variability increasing. Recommend nozzle inspection within 2 cycles. Parts lead time: 14 days. Schedule maintenance now to avoid failure."

### Scenario 3: False Positive (Sensor Malfunction)
- Rotor balance suddenly spikes to 0.9g (outside limits)
- Temperature, pressure, vibration all normal
- No historical pattern match
- **Agent output:** "ALERT: Rotor balance sensor reading suspect. Request sensor recalibration/verification before maintenance action. No equipment maintenance recommended."

### Scenario 4: Ambiguous Case (Multiple Competing Hypotheses)
- Fuel pressure σ increasing + temperature spiking
- Could be fuel nozzle wear (85% confidence) OR blade fouling + thermal stress (70% confidence)
- Both precede combustor failure but with different corrective actions
- **Agent output:** "Multiple competing diagnoses detected. Recommend: (1) Visual inspection of fuel nozzles (2-hour check), (2) If nozzles normal, inspect compressor blade fouling. Confidence split: 60% nozzle wear / 40% blade fouling."

---

## **8. WHITEBOARD VISUALIZATION**

```
┌─────────────────────────────────────────────────────────────────┐
│        AIRCRAFT ENGINE MANUFACTURING: SIX SIGMA VARIABILITY      │
│                  Process Drift → Failure Prevention              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  INPUT (Sensors)          AGENTS                  OUTPUT         │
│  ───────────────────────────────────────────────────────────────│
│                                                                   │
│  • Fuel Pressure      ┌─ Signal Agent (SPC)    Cpk Trending     │
│  • Temp/Pressure      │  ├─ Calculate Cpk      "Degrading"      │
│  • Rotor Balance      │  ├─ Detect σ drift     Alert if >80%    │
│  • Blade Clearance    │  └─ Flag SPC violations of tolerance   │
│  • Coating Thickness  │                                         │
│                       ├─ Asset-Context Agent   Time-to-Failure │
│  Real-time PLC        │  ├─ Wear curves        "15 cycles @"    │
│  streams              │  ├─ Service history    "current drift"  │
│  (10Hz sampling)      │  └─ Maintenance windows               │
│                       │                                         │
│                       ├─ Knowledge Agent       CTQ Mapping      │
│                       │  ├─ Parse specs        "5 failure modes │
│                       │  ├─ FMEA ranking       linked"          │
│                       │  └─ Safety prerequisites               │
│                       │                                         │
│                       ├─ Root-Cause Agent      Ranked Hypotheses│
│                       │  ├─ Pareto 80/20       "(1) Nozzle 85% │
│                       │  ├─ Correlation match  (2) Fouling 10% │
│                       │  └─ Historical patterns(3) Seal 5%"     │
│                       │                                         │
│                       └─ Work-Instruction      Action Plan      │
│                          ├─ Preventive steps   "Replace nozzles│
│                          ├─ Parts + lead time  in 14 days"     │
│                          └─ Escalation logic   "Cost: $2K"     │
│                                                                   │
├─────────────────────────────────────────────────────────────────┤
│                      FEEDBACK LOOP                                │
│  Outcome (success/failure) → Update wear curves → Improve Cpk    │
└─────────────────────────────────────────────────────────────────┘
```

---

## **9. RESPONSIBLE AI & GUARDRAILS**

- ✅ **Never bypass industrial safety procedures** (lockout/tagout must complete first)
- ✅ **No autonomous actuation or PLC write-back** (recommendations only)
- ✅ **Isolate OT interfaces** (read-only mock connectors)
- ✅ **Defense against prompt injection** (sanitize manual documents)
- ✅ **Operator acknowledgment required** at critical decision points
- ✅ **Audit trail** (all recommendations logged with timestamps and confidence scores)

---

## **10. SUCCESS CRITERIA (DEFINITION OF DONE)**

- ✅ **Diagnosis:** Top-3 root causes ranked by confidence, tied to supporting evidence
- ✅ **Cpk Detection:** Identify degradation ≥2 cycles before traditional alert
- ✅ **Work Instructions:** Include lockout, verification checkpoints, escalation rules
- ✅ **Parts Validation:** References to part numbers, lead times, inventory status
- ✅ **Feedback Loop:** Failed/successful outcomes logged without altering approved manuals
- ✅ **Demo Coverage:**
  - Normal operation (no alerts)
  - Gradual wear (preventive action recommended)
  - False positive (sensor malfunction)
  - Ambiguous case (competing hypotheses)

---

## **11. FINANCIAL IMPACT SUMMARY**

### Cost of Current Approach (Manual Diagnosis)
- **Unplanned downtime:** 27 hours/month per facility
- **Cost per hour:** $260K-$2.3M (aerospace/engine manufacturing)
- **Monthly cost:** $7-15M per facility
- **Annual exposure:** $84-180M per facility
- **Time to diagnosis:** 4 hours (production stalled)

### Cost with Six Sigma Predictive Solution
- **Early detection:** ≥2 cycles before failure (15-30 days warning)
- **Reduced downtime:** 10-15 hours/month (40-50% reduction)
- **Monthly savings:** $4-8M per facility
- **Annual savings:** $48-108M per facility
- **Time to diagnosis:** 15 minutes (16x faster)

### Additional Benefits
- ✅ Reduced scrap/rework (FPY improvement: 95% → 98%)
- ✅ Fewer catastrophic engine failures (prevents $500K rebuilds)
- ✅ Improved asset reliability (Cpk from 1.1 → 1.67)
- ✅ Operator confidence in maintenance decisions
- ✅ Regulatory compliance (AS9100, FAA documentation)

---

## **12. NEXT STEPS**

1. **Finalize mock data** (sensor time-series, CTQ specs, FMEA register, 50+ labeled cases)
2. **Build agent prototypes** (SPC monitor, wear predictor, root-cause ranker)
3. **Integrate multi-agent orchestration** (message routing, decision logic)
4. **Develop SPC dashboard** (real-time Cpk, control charts, alerts)
5. **Create work-instruction generator** (safety-compliant procedures)
6. **Design digital-twin simulation** (validate preventive actions before operator approval)
7. **Test on labeled failure scenarios** (accuracy evaluation vs. expert diagnosis)
8. **Document audit trail** (regulatory compliance for AS9100/FAA)

---

**Document Created:** 2026-09-11  
**Use Case:** Aircraft Engine Manufacturing (Six Sigma Process Variability)  
**Domain:** Rolls-Royce, GE Aviation, Pratt & Whitney  
**Goal:** Reduce unplanned downtime 40-50% ($48-108M annual savings per facility)
