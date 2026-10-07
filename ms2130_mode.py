#!/usr/bin/env python3
"""Print the MS2130's progressive video timing, signaling type and sync polarities."""

import hid


def readaddr(device, addr):
    request = bytes((0, 0xB5, addr >> 8, addr & 255, 0, 0, 0, 0, 0))
    if device.send_feature_report(request) != len(request):
        raise OSError("MS2130 HID write failed")
    reply = bytes(device.get_feature_report(0, 9))
    if len(reply) != 9 or reply[:4] != request[:4]:
        raise OSError(f"MS2130 HID read failed at {addr:#06x}")
    return int.from_bytes(reply[4:6], "little"), int.from_bytes(reply[6:8], "little")


devices = hid.enumerate(0x345F, 0x2130)
if len(devices) != 1:
    raise SystemExit(f"Expected one MS2130 HID interface, found {len(devices)}")

device = hid.device()
try:
    device.open_path(devices[0]["path"])
    period = readaddr(device, 0xE148)[1]  # HDMI line period in 384 MHz ticks
    regs = {addr: readaddr(device, addr) for addr in
            (0xE14C, 0xE150, 0xE168, 0xE170, 0xE184, 0xE188,
             0xE18C, 0xE190, 0xE194, 0x23AC, 0x23DC)}
    period_end = readaddr(device, 0xE148)[1]
finally:
    device.close()

width, hblank = regs[0xE184]
hfront, hsync = regs[0xE188]
height, vblank = regs[0xE18C]
vfront, vsync = regs[0xE190]
vback = regs[0xE194][0]
polarity = regs[0x23AC][0]
hdmi = regs[0x23DC][0] & 1

htotal, vtotal = width + hblank, height + vblank
if not (period and period_end and abs(period - period_end) <= 5
        and width and height and hsync and vsync
        and hfront + hsync <= hblank and vfront + vsync + vback == vblank
        and regs[0xE14C][1] == htotal and regs[0xE150][0] == width
        and regs[0xE168][0] == height and regs[0xE170][0] == vtotal):
    raise SystemExit("No stable HDMI input timing detected")

clock_mhz = 384 * htotal / period
print(f"Pixel clock (MHz): {clock_mhz:.3f}"
      f"\nRefresh rate (Hz): {clock_mhz * 1_000_000 / (htotal * vtotal):.3f}"
      f"\nInput signaling: {'HDMI' if hdmi else 'DVI'}"
      f"\nHorizontal active (pixels): {width}"
      f"\nHorizontal front porch (pixels): {hfront}"
      f"\nHorizontal sync width (pixels): {hsync}"
      f"\nHorizontal back porch (pixels): {hblank - hfront - hsync}"
      f"\nHorizontal sync polarity: {'+' if polarity & 0x02 else '-'}"
      f"\nHorizontal total (pixels): {htotal}"
      f"\nVertical active (lines): {height}"
      f"\nVertical front porch (lines): {vfront}"
      f"\nVertical sync width (lines): {vsync}"
      f"\nVertical back porch (lines): {vback}"
      f"\nVertical sync polarity: {'+' if polarity & 0x04 else '-'}"
      f"\nVertical total (lines): {vtotal}")
