# CLAUDE.md - Precursor LoRa Expansion Module

## Project Status

**Phase:** Initial design complete, ready for KiCad verification

**NextPCB Accelerator #5:** APPROVED - Submit order within ~1 week

## Quick Start

1. Open `hardware/precursor-lora.kicad_pro` in KiCad 8
2. Verify schematic connectivity and run ERC
3. Import symbol/footprint libraries if needed
4. Create PCB layout from schematic
5. Run DRC, fix any issues
6. Generate Gerbers and verify in NextPCB viewer
7. Submit order

## Key Design Decisions

- **RAK3172** selected over alternatives for integrated STM32WLE5 SoC
- **UART interface** (not SPI) for simplicity with Precursor FPGA
- **AP2112K LDO** for efficiency and low quiescent current
- **2-layer PCB** sufficient for this low-frequency design
- **50x30mm board** fits Precursor battery compartment with margin

## Component Sources

| Part | Best Source | Notes |
|------|-------------|-------|
| RAK3172 | RAKwireless, DigiKey | ~$6.50 |
| AP2112K-3.3 | LCSC C51118 | $0.15 |
| Passives | LCSC | Basic parts |
| U.FL | LCSC C88374 | Hirose compatible |

## Files That Need Human Verification

1. `hardware/precursor-lora.kicad_sch` - Open in KiCad, verify connections
2. `hardware/symbols/RAK3172.kicad_sym` - Verify pinout against datasheet
3. `hardware/footprints.pretty/RAK3172.kicad_mod` - Verify dimensions

## PCB Layout Guidelines

- RAK3172 center-top of board
- LDO and power section left side
- Connector at bottom edge
- U.FL connector right side, near RAK3172 RF pin
- Ground plane on bottom layer
- Keep RF trace <10mm, 50Ω impedance

## What Claude Code Cannot Do

- Run KiCad GUI (must be done by human)
- Generate Gerber files (requires KiCad)
- Visual verification of layout
- Upload to NextPCB

## Verification Checklist

### Before Layout
- [ ] Open schematic in KiCad
- [ ] Run ERC, fix any issues
- [ ] Verify all component footprints assigned

### After Layout
- [ ] Run DRC, fix violations
- [ ] Check RF trace routing (short, over ground)
- [ ] Verify connector placement accessible
- [ ] Add version/date to silkscreen
- [ ] Check board fits 50x30mm

### Before Order
- [ ] Generate Gerbers
- [ ] View in NextPCB viewer
- [ ] Verify drill file present
- [ ] Upload BOM to NextPCB
- [ ] Verify all parts in stock
