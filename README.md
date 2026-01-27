# Precursor LoRa Expansion Module

A production-ready LoRa radio expansion module for the [Precursor](https://www.crowdsupply.com/sutajio-kosagi/precursor) open-source secure computing platform.

## Overview

This module adds LoRaWAN connectivity to the Precursor device, enabling 15km+ range communication without WiFi/Bluetooth attack surface. It fits in the Precursor's battery compartment and connects via the internal GPIO header.

## Features

- **RAK3172 LoRaWAN Module** - Based on STM32WLE5CC with integrated LoRa radio
- **Frequency Bands** - EU868, US915, AU915, AS923, and more
- **Long Range** - 15km+ line-of-sight with proper antenna
- **Low Power** - <2µA sleep current, ideal for battery operation
- **Simple Interface** - UART AT command interface to Precursor FPGA
- **Compact Design** - Fits in Precursor battery compartment (50x30mm)

## Specifications

| Parameter | Value |
|-----------|-------|
| Input Voltage | 3.7V (LiPo battery) |
| Regulated Voltage | 3.3V via AP2112K LDO |
| Interface | UART (115200 baud default) |
| TX Current | ~100mA peak |
| RX Current | ~5mA |
| Sleep Current | <2µA |
| Board Size | 50mm x 30mm |
| Layers | 2 |

## Pin Connections

| Precursor GPIO | RAK3172 Pin | Function |
|----------------|-------------|----------|
| GPIO0 | PB7 | UART1_RX (data to RAK) |
| GPIO1 | PB6 | UART1_TX (data from RAK) |
| GPIO2 | RST | Module reset (active low) |
| GPIO3 | PB5 | Busy/Status indicator |
| 3V7 | VIN | Power input |
| GND | GND | Ground |

## Bill of Materials

| Ref | Part | Value | Package | Qty | Est. Cost |
|-----|------|-------|---------|-----|-----------|
| U1 | RAK3172 | - | LGA-32 | 1 | $6.50 |
| U2 | AP2112K-3.3 | 3.3V LDO | SOT-23-5 | 1 | $0.30 |
| C1, C2 | Capacitor | 10µF | 0603 | 2 | $0.04 |
| C3, C4 | Capacitor | 100nF | 0402 | 2 | $0.02 |
| R1, R2 | Resistor | 10K | 0402 | 2 | $0.02 |
| R3 | Resistor | 1K | 0402 | 1 | $0.01 |
| J1 | Header | 8-pin | 1.27mm | 1 | $1.50 |
| J2 | U.FL | RF | U.FL | 1 | $0.80 |
| LED1 | LED | Green | 0603 | 1 | $0.05 |
| **Total** | | | | | **~$9.24** |

## Directory Structure

```
PrecursorLoRa/
├── README.md                 # This file
├── hardware/
│   ├── precursor-lora.kicad_pro    # KiCad 8 project
│   ├── precursor-lora.kicad_sch    # Schematic
│   ├── precursor-lora.kicad_pcb    # PCB layout
│   ├── symbols/                    # Custom symbols
│   └── footprints.pretty/          # Custom footprints
├── fabrication/
│   ├── gerbers/                    # Gerber files for manufacturing
│   ├── bom/                        # Bill of Materials
│   └── pick-and-place/             # Assembly positions
├── docs/
│   └── assembly-notes.md           # Assembly instructions
└── datasheets/                     # Component datasheets (not tracked)
```

## Manufacturing

This board is designed for the **NextPCB Accelerator** free prototype program.

### Design Rules (NextPCB Compatible)
- Minimum trace width: 0.2mm
- Minimum trace spacing: 0.2mm
- Minimum via drill: 0.3mm
- Minimum via pad: 0.6mm
- PCB thickness: 1.6mm
- Copper weight: 1oz
- Surface finish: HASL or ENIG

### Generating Gerbers

1. Open `hardware/precursor-lora.kicad_pcb` in KiCad 8
2. File → Plot → Select Gerber output
3. Include layers: F.Cu, B.Cu, F.Paste, B.Paste, F.SilkS, B.SilkS, F.Mask, B.Mask, Edge.Cuts
4. Generate drill files (Excellon format)
5. Zip all files for upload

## Assembly Notes

See [docs/assembly-notes.md](docs/assembly-notes.md) for detailed assembly instructions.

Key points:
- RAK3172 module has orientation marking (pin 1 dot)
- Apply flux for castellated pad soldering
- Keep RF trace short and over ground plane
- Test continuity before powering

## Usage with Precursor

The module communicates via UART AT commands. Example initialization:

```
AT+NWM=1              # Set LoRaWAN mode
AT+NJM=1              # Set OTAA join mode
AT+DEVEUI=<your_eui>  # Set device EUI
AT+APPEUI=<app_eui>   # Set application EUI
AT+APPKEY=<app_key>   # Set application key
AT+JOIN              # Join network
AT+SEND=1:<data>     # Send data on port 1
```

## License

This project is licensed under **CERN-OHL-P v2** (CERN Open Hardware Licence Version 2 - Permissive).

You are free to use, modify, and distribute this design for any purpose.

## Resources

- [RAK3172 Datasheet](https://docs.rakwireless.com/product-categories/wisduo/rak3172-module/datasheet/)
- [Precursor Hardware](https://github.com/betrusted-io/betrusted-hardware)
- [AP2112K Datasheet](https://www.diodes.com/assets/Datasheets/AP2112.pdf)
- [NextPCB Gerber Viewer](https://www.nextpcb.com/free-online-gerber-viewer.html)

## Author

Designed for the Precursor community.

---

*Built with KiCad 8 | NextPCB Accelerator #5*
