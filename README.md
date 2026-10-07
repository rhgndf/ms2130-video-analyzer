# MS2130 HDMI input timing

Example with a 1920×1080 @ 60 Hz input:

```text
Pixel clock (MHz): 148.497
Refresh rate (Hz): 59.999
Input signaling: HDMI
Horizontal active (pixels): 1920
Horizontal front porch (pixels): 88
Horizontal sync width (pixels): 44
Horizontal back porch (pixels): 148
Horizontal sync polarity: +
Horizontal total (pixels): 2200
Vertical active (lines): 1080
Vertical front porch (lines): 4
Vertical sync width (lines): 5
Vertical back porch (lines): 36
Vertical sync polarity: +
Vertical total (lines): 1125
```

## Requirements

`hidapi` python package

## Details

Clock are estimates, so their last digits may vary.

## Credits

- [ms-tools](ms-tools/) documents the MS2130 factory HID RAM-read protocol and input-resolution registers.