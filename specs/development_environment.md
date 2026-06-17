# Development Environment & Hardware Target

Status: DRAFT — open questions noted below.

## Intent

MPF rules run on a Raspberry Pi controlling real hardware. Development happens
on a Mac without physical hardware. A separate visual UI (GMC) provides an
interactive playfield for manual testing during development. The RPU v102 board
bridges the Pi to the original machine wiring using a standard, documented
serial protocol.

---

## Environment layers

### Mac (development)

MPF runs with the `smart_virtual` platform ([config/config_dev.yaml](../config/config_dev.yaml)):

- All hardware (switches, coils, lights) is emulated inside MPF itself.
- GMC (Godot Media Controller, [gmc/](../gmc/)) connects over BCP on localhost:5050
  and provides a clickable playfield for interactive manual testing.
- Rule testing (unit tests under `tests/`) does not need GMC — tests drive switches
  programmatically via the MPF test harness.
- Segment display text is forwarded to GMC over BCP via
  `virtual_segment_display_connector` (dev-only; on real hardware LISY drives
  the physical displays directly).

**GMC's role is the interactive development UI, not the rules emulator.**
The emulation is `smart_virtual` inside MPF. GMC is layered on top for
visibility and manual switch input.

### Raspberry Pi (production)

MPF runs with the `lisy` platform ([config/config_rpi.yaml](../config/config_rpi.yaml)):

- All hardware I/O (switches, coils, lights, displays) is handled by the LISY
  platform driver communicating over serial with the RPU v102 board.
- No window / no GUI (`auto_create_window: false`).
- Serial connection: `/dev/ttyUSB0` at 115200 baud.

---

## RPU v102 and LISY protocol

The RPU v102 board sits between the Pi and the original Stern Trident wiring
harness. MPF talks to it using the LISY protocol over USB serial.

LISY is an open, documented protocol originally designed for LISY80/LISY35
boards running MPF on classic arcade/pinball machines. Using it here means:

- MPF's existing `lisy` platform driver works without modification.
- The protocol is documented and implementable by other frameworks; other
  frameworks do not natively speak LISY, but the serial transport and protocol
  spec make an adapter feasible.
- The RPU firmware (Arduino/microcontroller layer on the RPU board) must
  implement the LISY protocol. **This firmware does not yet exist** — it is
  listed as a next step in the README.

---

## Open questions

### Does GMC need to run on the Pi?

For the 1979 Trident hardware:

- **Displays**: The Trident uses 6-digit 7-segment displays. LISY drives these
  natively over serial. GMC is not needed for displays on the Pi.
- **Sound**: The original machine uses a solenoid-based chime/tone board.
  MPF's built-in sound system can drive audio on the Pi (ALSA/PulseAudio)
  without GMC. GMC on the Pi would only be needed for richer media (samples,
  music, video).

Decision needed: does the production Pi deployment use original-style chimes
(no GMC needed on Pi) or richer MPF-managed audio (GMC on Pi)?

---

## Summary of code alignment

| Intent | Confirmed? | Where |
|---|---|---|
| MPF on Raspberry Pi | Yes | `config/config_rpi.yaml` |
| Mac dev without hardware | Yes | `config/config_dev.yaml`, `smart_virtual` |
| GMC for interactive testing | Yes | `gmc/`, BCP on localhost:5050 |
| RPU via LISY over serial | Yes (config only) | `config_rpi.yaml`, `/dev/ttyUSB0` |
| RPU firmware speaks LISY | Not yet | README "Next Steps" item 1 |
| LISY is standard/portable protocol | Mostly | Open; documented but MPF-native |
| GMC on Pi for sounds/displays | Not decided | See open questions above |
