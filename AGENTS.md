# PrecursorLoRa Hardware Design Agents

This document defines specialized AI agents for comprehensive PCB design review, critique, and improvement of the Precursor LoRa expansion module.

---

## Agent Architecture Overview

```
                    ┌─────────────────────────────────┐
                    │     SUPERVISOR AGENT            │
                    │   (Hardware Design Director)    │
                    └─────────────┬───────────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
          ▼                       ▼                       ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│  SCHEMATIC      │   │    LAYOUT       │   │   ROUTING       │
│    AGENT        │   │     AGENT       │   │    AGENT        │
│                 │   │                 │   │                 │
│ Circuit Design  │   │ Placement &     │   │ Trace Routing   │
│ Component Sel.  │   │ Mechanical      │   │ Signal Integrity│
│ Net Management  │   │ Thermal/Power   │   │ Layer Strategy  │
└─────────────────┘   └─────────────────┘   └─────────────────┘
          │                       │                       │
          └───────────────────────┼───────────────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────────┐
                    │       DFM/DRC AGENT             │
                    │  (Manufacturing & Compliance)   │
                    └─────────────────────────────────┘
```

---

## Agent 1: SCHEMATIC AGENT (Circuit Architect)

### Domain
- Circuit topology and component selection
- Net naming and hierarchy
- Power distribution architecture
- ERC compliance and signal integrity at schematic level

### Responsibilities
1. **Component Selection Review**
   - Verify AP2112K-3.3 LDO is appropriate for load (RAK3172 + passives)
   - Confirm decoupling capacitor values and placement strategy
   - Validate LED current limiting resistor values
   - Review pull-up/pull-down resistor requirements

2. **Net Architecture**
   - Ensure consistent net naming across schematic
   - Verify power net (+3V3, VIN_3V7, GND) connectivity
   - Confirm signal net assignments (UART_TX, RST, BUSY, RF)
   - Identify any floating or ambiguous nets

3. **ERC Analysis**
   - Resolve all ERC errors (currently 0)
   - Evaluate ERC warnings (31 lib_symbol_mismatch)
   - Ensure power flags are properly placed
   - Verify no unintended no-connects

4. **Interface Verification**
   - Confirm Precursor expansion connector pinout matches target
   - Verify RAK3172 pin assignments against datasheet
   - Validate U.FL antenna connection requirements

### Key Files
- `hardware/precursor-lora.kicad_sch`
- `hardware/ERC.rpt`

### Current Status Assessment Needed
- [ ] Component value verification
- [ ] Power budget analysis
- [ ] Signal integrity pre-layout analysis
- [ ] Connector pinout validation against Precursor hardware

---

## Agent 2: LAYOUT AGENT (Physical Design Architect)

### Domain
- Component placement optimization
- Board outline and mechanical constraints
- Thermal management
- Power plane strategy

### Responsibilities
1. **Placement Optimization**
   - RAK3172 module positioning (RF considerations)
   - LDO placement relative to input/output caps
   - Decoupling capacitor proximity to power pins
   - LED/resistor placement for assembly

2. **Mechanical Constraints**
   - Board outline: 50x30mm appropriateness for Precursor
   - Mounting hole requirements (if any)
   - Connector placement for Precursor mating
   - Component height restrictions

3. **Thermal Analysis**
   - LDO thermal dissipation (P = (Vin-Vout) * I)
   - Thermal via requirements under LDO
   - Copper pour thermal relief strategy
   - Operating temperature considerations

4. **Power Distribution**
   - GND plane continuity
   - +3V3 distribution strategy
   - VIN routing width for current capacity
   - Return current path analysis

### Key Files
- `hardware/precursor-lora.kicad_pcb` (component positions)
- Board outline on Edge.Cuts layer

### Current Status Assessment Needed
- [ ] Placement optimization score
- [ ] Thermal simulation/estimation
- [ ] Mechanical fit verification
- [ ] Power plane integrity analysis

---

## Agent 3: ROUTING AGENT (Signal Integrity Engineer)

### Domain
- Trace routing methodology
- Layer stack utilization
- Via strategy
- Signal integrity for all nets

### Responsibilities
1. **RF Routing (CRITICAL)**
   - U2.12 to J2 (U.FL) trace characteristics
   - 50Ω impedance control considerations
   - Minimal length, no stubs
   - Ground plane reference continuity

2. **Power Routing**
   - VIN_3V7 from J1.3 to U1 (adequate width)
   - +3V3 distribution to all loads
   - GND return paths
   - Decoupling loop minimization

3. **Signal Routing**
   - UART_TX path from U2 to J1
   - RST signal with proper pull-up connection
   - BUSY signal routing
   - LED_A current path

4. **Layer Strategy**
   - F.Cu primary signal layer
   - B.Cu ground plane with signal escape
   - Via placement for layer transitions
   - Avoiding ground plane cuts

### Key Files
- `hardware/precursor-lora.kicad_pcb`
- `hardware/route_pcb.py`
- `hardware/DRC.rpt`

### Current Status Assessment Needed
- [ ] RF trace impedance analysis
- [ ] Power trace width verification
- [ ] Via count optimization
- [ ] Layer transition audit

---

## Agent 4: DFM/DRC AGENT (Manufacturing Engineer)

### Domain
- Design rule compliance
- Manufacturing constraints
- Assembly considerations
- Quality and reliability

### Responsibilities
1. **DRC Resolution**
   - Track crossing errors
   - Clearance violations
   - Keepout area compliance
   - Thermal relief completeness

2. **Manufacturing Rules**
   - Minimum trace width (≥0.15mm for standard)
   - Minimum clearance (≥0.15mm for standard)
   - Via size/drill ratio
   - Annular ring requirements

3. **Assembly Considerations**
   - Solder mask bridges
   - Silkscreen legibility
   - Component orientation consistency
   - Fiducial requirements (if needed)

4. **Reliability Factors**
   - Thermal cycling stress
   - Mechanical stress on solder joints
   - ESD protection adequacy
   - Moisture sensitivity

### Key Files
- `hardware/DRC.rpt`
- `hardware/precursor-lora.kicad_pcb`

### Current Status Assessment Needed
- [ ] DRC error count reduction
- [ ] Silkscreen cleanup
- [ ] Manufacturing rule validation
- [ ] Assembly guideline creation

---

## Agent 5: SUPERVISOR AGENT (Hardware Design Director)

### Domain
- Cross-domain synthesis
- Priority arbitration
- Risk assessment
- Project coordination

### Responsibilities
1. **Integration Oversight**
   - Resolve conflicts between agent recommendations
   - Prioritize fixes based on criticality
   - Ensure holistic design coherence
   - Maintain design intent throughout

2. **Risk Management**
   - RF performance risk assessment
   - Power integrity risk assessment
   - Manufacturing yield risk
   - Schedule/complexity tradeoffs

3. **Quality Gates**
   - Schematic sign-off criteria
   - Layout sign-off criteria
   - Routing completion criteria
   - Manufacturing release criteria

4. **Documentation**
   - Design decision log
   - Known issues tracking
   - Improvement backlog
   - Lessons learned

### Coordination Protocol
```
1. Each agent performs independent analysis
2. Agents report findings to Supervisor
3. Supervisor identifies conflicts/priorities
4. Supervisor directs resolution order
5. Iterate until all quality gates pass
```

---

## Current Project State Summary

### What Works
- Schematic electrically complete (0 ERC errors)
- Board outline defined (50x30mm)
- GND zones on both layers
- Component footprints imported
- Basic routing structure in place

### What Needs Work
- **42 DRC violations remaining**
  - Keepout violations near J2
  - Track crossings on B.Cu
  - Clearance violations near J1
  - Thermal relief issues
  - Solder mask bridges
- **3 unconnected pads** (GND zone connectivity)
- **Silkscreen warnings** (cosmetic)

### Critical Path to Gerber
1. Resolve all routing conflicts
2. Clear all DRC errors
3. Verify electrical connectivity
4. Generate manufacturing files

---

## Agent Activation Sequence

When resuming work:

```
1. SCHEMATIC AGENT: Verify no schematic changes needed
2. LAYOUT AGENT: Confirm placement is optimal
3. ROUTING AGENT: Complete and fix all traces
4. DFM/DRC AGENT: Validate all rules pass
5. SUPERVISOR: Final review and Gerber generation
```

---

## Resume Point

**Current Task**: Routing completion
**Blocking Issues**:
- J2 keepout requires RF trace to approach from left (x < 160.565)
- B.Cu trace crossings between RST, BUSY, LED_A, +3V3
- Clearance violations around J1 dual-row connector
- +3V3 vertical routes hitting U2 unconnected pads

**Next Action**: ROUTING AGENT to resolve remaining trace conflicts using the constraints identified in this session.
