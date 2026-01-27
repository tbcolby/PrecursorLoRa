# Assembly Notes - Precursor LoRa Expansion Module

## Component Orientation

### U1 - RAK3172 Module
- Pin 1 is marked with a dot on the module corner
- Align pin 1 dot with the silkscreen marker on PCB
- Module dimensions: 15.5mm x 15mm
- Castellated edge pads - apply flux generously before soldering

### U2 - AP2112K-3.3 LDO
- SOT-23-5 package
- Pin 1 indicated by chamfered corner
- Match orientation with silkscreen

### J2 - U.FL Connector
- Center pin is RF signal
- Shield connects to ground
- Ensure good solder joints on all ground tabs

## Soldering Sequence (Recommended)

1. **RAK3172 (U1)** - Largest component, solder first
   - Apply flux to all pads
   - Tack one corner pad
   - Verify alignment
   - Solder remaining pads
   - Use hot air or drag soldering

2. **LDO (U2)** - SOT-23-5
   - Standard SMD soldering

3. **Capacitors (C1-C4)** - 0603 and 0402
   - C1, C2: 10µF input/output caps near LDO
   - C3, C4: 100nF decoupling near RAK3172

4. **Resistors (R1-R3)** - 0402
   - R1: Reset pullup (10K)
   - R2: BOOT0 pulldown (10K)
   - R3: LED current limit (1K)

5. **LED (LED1)** - 0603
   - Check polarity (cathode mark)

6. **U.FL Connector (J2)**
   - Solder center pin first
   - Then ground tabs

7. **Header (J1)** - 1.27mm pitch
   - Verify alignment before soldering all pins

## Pre-Power Checklist

- [ ] Visual inspection for solder bridges
- [ ] Check RAK3172 orientation (pin 1)
- [ ] Verify U.FL connector is secure
- [ ] Continuity test: VIN to U2 input
- [ ] Continuity test: 3.3V rail to RAK3172 VDD
- [ ] No shorts between VIN/3V3 and GND

## Initial Power-Up Test

1. Connect multimeter to 3.3V test point
2. Apply 3.7V input (current limited to 100mA)
3. Verify 3.3V output (should be 3.28-3.32V)
4. Current draw should be ~5-10mA (module idle)
5. LED should illuminate

## UART Communication Test

Connect USB-UART adapter:
- Adapter TX → J1 pin (UART_RX / PB7)
- Adapter RX → J1 pin (UART_TX / PB6)
- Adapter GND → J1 GND

Terminal settings:
- Baud: 115200
- Data: 8 bits
- Parity: None
- Stop: 1 bit

Test command:
```
AT
```
Expected response:
```
OK
```

## Troubleshooting

### No 3.3V Output
- Check U2 solder joints
- Verify input voltage present
- Check for shorts on 3.3V rail

### No UART Response
- Verify TX/RX not swapped
- Check BOOT0 is pulled LOW (normal operation)
- Try reset sequence (pull RST low, release)
- Check baud rate

### Module Gets Hot
- Likely short circuit
- Remove power immediately
- Inspect for solder bridges under RAK3172

### LED Not Lit
- Check LED orientation
- Verify 3.3V present
- Check R3 solder joints

## RF Performance Tips

- Keep U.FL pigtail short (<10cm) to antenna
- Use 50Ω matched antenna for your frequency band
- Ground plane should extend under RF trace
- Keep switching power supplies away from RF section
