#!/usr/bin/env python3
"""Generate trace routing for precursor-lora PCB - KEEPOUT-AWARE VERSION."""

import re
import hashlib

NET_GND = 1
NET_3V3 = 2
NET_VIN = 3
NET_BUSY = 4
NET_UART = 5
NET_RST = 7
NET_RF = 8
NET_LED = 9

TW = 0.25
VIA_SIZE = 0.6
VIA_DRILL = 0.3

FCU = "F.Cu"
BCU = "B.Cu"

segments = []
vias = []
_uuid_counter = 0


def seg(x1, y1, x2, y2, net, layer=FCU, width=TW):
    segments.append((x1, y1, x2, y2, net, layer, width))


def via(x, y, net):
    vias.append((x, y, net))


def generate_uuid():
    global _uuid_counter
    _uuid_counter += 1
    h = hashlib.md5(f"pcb-{_uuid_counter:08d}".encode()).hexdigest()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


# ============================================================
# J2 KEEPOUT: x=160.565-162.655, y=99.55-101.45
# Must approach J2.1 (160.03, 100.5) from LEFT (x < 160.565)
# ============================================================

# ============================================================
# NET 8 - RF: U2.12 (145.07, 92.395) -> J2.1 (160.03, 100.5)
# Stay left of keepout - approach from x=159
# ============================================================
seg(145.07, 92.395, 159.0, 92.395, NET_RF, FCU, 0.3)   # right along U2 top
seg(159.0, 92.395, 159.0, 100.5, NET_RF, FCU, 0.3)     # down
seg(159.0, 100.5, 160.03, 100.5, NET_RF, FCU, 0.3)     # right to J2.1

# ============================================================
# NET 5 - UART: J1.1 <-> J1.7 <-> U2.4
# Avoid U2 right-side pads - use wider clearance
# ============================================================
seg(160.63, 92.0, 159.5, 92.0, NET_UART, FCU)
seg(159.5, 92.0, 159.5, 95.81, NET_UART, FCU)
seg(159.5, 95.81, 160.63, 95.81, NET_UART, FCU)

# J1.7 to U2.4 on B.Cu
seg(160.63, 95.81, 159.5, 95.81, NET_UART, BCU)
seg(159.5, 95.81, 140.0, 95.81, NET_UART, BCU)
seg(140.0, 95.81, 140.0, 101.8, NET_UART, BCU)
via(140.0, 101.8, NET_UART)
seg(140.0, 101.8, 141.765, 101.8, NET_UART, FCU)

# ============================================================
# NET 7 - RST: J1.5, U2.22, R2.2, R3.1, R3.2
# Separate RST via from UART path
# ============================================================
# R2/R3 cluster
seg(160.5, 106.51, 160.5, 108.5, NET_RST, FCU)
seg(160.5, 108.5, 159.48, 108.5, NET_RST, FCU)

# J1.5 to U2.22 - use different path to avoid UART
seg(160.63, 94.54, 158.0, 94.54, NET_RST, BCU)
seg(158.0, 94.54, 158.0, 96.5, NET_RST, BCU)           # down past UART at y=95.81
via(158.0, 96.5, NET_RST)
seg(158.0, 96.5, 157.265, 96.5, NET_RST, FCU)          # left on F.Cu
seg(157.265, 96.5, 157.265, 95.45, NET_RST, FCU)       # up to U2.22

# J1.5 to R2/R3 via B.Cu right side
seg(160.63, 94.54, 163.0, 94.54, NET_RST, BCU)
seg(163.0, 94.54, 163.0, 106.51, NET_RST, BCU)
via(163.0, 106.51, NET_RST)
seg(163.0, 106.51, 160.5, 106.51, NET_RST, FCU)

# ============================================================
# NET 2 - +3V3
# Use x=155 for R1/R2 vertical to avoid U2 pads at x=157.265
# ============================================================
seg(161.9, 94.54, 164.0, 94.54, NET_3V3, FCU)
seg(164.0, 94.54, 164.0, 114.0, NET_3V3, FCU)

# U2.24 (157.265, 97.99) - branch left from trunk
seg(164.0, 97.99, 157.265, 97.99, NET_3V3, FCU)

# R1.1 and R2.1 - vertical at x=155 (clear of U2 pads)
seg(164.0, 114.0, 136.5, 114.0, NET_3V3, FCU)          # bottom bus
seg(155.0, 114.0, 155.0, 104.52, NET_3V3, FCU)         # up at x=155
seg(155.0, 104.52, 159.48, 104.52, NET_3V3, FCU)       # right to R1.1
seg(155.0, 106.51, 159.48, 106.51, NET_3V3, FCU)       # right to R2.1

# C3/C4 at x=153.62
seg(153.62, 114.0, 153.62, 109.65, NET_3V3, FCU)

# C2 at x=145.835
seg(145.835, 114.0, 145.835, 112.43, NET_3V3, FCU)

# U1.5 at x=143.1675 - approach from right to avoid hitting pad4 below
seg(144.5, 114.0, 144.5, 110.115, NET_3V3, FCU)        # up at x=144.5
seg(144.5, 110.115, 143.1675, 110.115, NET_3V3, FCU)   # left to U1.5

# U2.5 (141.765, 100.53) - use B.Cu to avoid crossings
via(164.0, 100.53, NET_3V3)
seg(164.0, 100.53, 142.5, 100.53, NET_3V3, BCU)
via(142.5, 100.53, NET_3V3)
seg(142.5, 100.53, 141.765, 100.53, NET_3V3, FCU)

# ============================================================
# NET 3 - VIN: J1.3, U1.1, U1.3, C1.1
# ============================================================
seg(160.63, 93.27, 137.5, 93.27, NET_VIN, BCU)
seg(137.5, 93.27, 137.5, 109.5, NET_VIN, BCU)
via(137.5, 109.5, NET_VIN)
seg(137.5, 109.5, 137.5, 112.015, NET_VIN, FCU)
seg(137.5, 110.115, 140.8925, 110.115, NET_VIN, FCU)   # right to U1.1
seg(137.5, 112.015, 140.8925, 112.015, NET_VIN, FCU)   # right to U1.3

# C1.1 connection on B.Cu
via(145.835, 109.92, NET_VIN)
seg(145.835, 109.92, 137.5, 109.92, NET_VIN, BCU)

# ============================================================
# NET 4 - BUSY: U2.30 (153.96, 107.395) -> J1.4 (161.9, 93.27)
# ============================================================
seg(153.96, 107.395, 153.96, 109.0, NET_BUSY, FCU)     # down
via(153.96, 109.0, NET_BUSY)
seg(153.96, 109.0, 165.0, 109.0, NET_BUSY, BCU)        # right on B.Cu
seg(165.0, 109.0, 165.0, 93.27, NET_BUSY, BCU)
seg(165.0, 93.27, 161.9, 93.27, NET_BUSY, BCU)

# ============================================================
# NET 9 - LED_A: LED1.2 (151.4475, 109.96) -> R1.2 (160.5, 104.52)
# ============================================================
via(151.4475, 109.96, NET_LED)
seg(151.4475, 109.96, 161.5, 109.96, NET_LED, BCU)
seg(161.5, 109.96, 161.5, 104.52, NET_LED, BCU)
via(161.5, 104.52, NET_LED)
seg(161.5, 104.52, 160.5, 104.52, NET_LED, FCU)


def format_segment(x1, y1, x2, y2, net, layer, width):
    return (
        f'\t(segment (start {x1} {y1}) (end {x2} {y2}) '
        f'(width {width}) (layer "{layer}") '
        f'(net {net}) (uuid "{generate_uuid()}"))'
    )


def format_via(x, y, net):
    return (
        f'\t(via (at {x} {y}) (size {VIA_SIZE}) (drill {VIA_DRILL}) '
        f'(layers "F.Cu" "B.Cu") '
        f'(net {net}) (uuid "{generate_uuid()}"))'
    )


def main():
    pcb_path = "/Volumes/PlexLaCie/Dev/Precursor/PrecursorLoRa/hardware/precursor-lora.kicad_pcb"
    with open(pcb_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == '(segment' or line.strip() == '(via':
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith(')'):
                j += 1
            i = j + 1
            continue
        elif '\t(segment (start' in line or '\t(via (at' in line:
            i += 1
            continue
        else:
            new_lines.append(line)
            i += 1

    content = ''.join(new_lines)
    content = re.sub(r'\n\n\n+', '\n\n', content)

    routing_lines = [""]
    for s in segments:
        routing_lines.append(format_segment(*s))
    routing_lines.append("")
    for v in vias:
        routing_lines.append(format_via(*v))

    insert_marker = "\n\t(embedded_fonts no)\n)"
    last_pos = content.rfind(insert_marker)
    if last_pos == -1:
        print("ERROR!")
        return

    new_content = content[:last_pos] + "\n" + "\n".join(routing_lines) + "\n" + content[last_pos:]

    with open(pcb_path, 'w') as f:
        f.write(new_content)

    print(f"Inserted {len(segments)} segments and {len(vias)} vias")


if __name__ == "__main__":
    main()
