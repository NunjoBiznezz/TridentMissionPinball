# Stern Trident - Mission Pinball Framework

This project configures Mission Pinball Framework (MPF) to work with a Stern Trident pinball machine using an RPU v102 board and LISY protocol.

## Hardware Setup

- **Machine**: Stern Trident
- **Controller Board**: RPU v102 with LISY protocol
- **Development Platform**: Laptop/Desktop
- **Production Platform**: Raspberry Pi

## Configuration Files

- `config.yaml` - Main MPF configuration
- `config_dev.yaml` - Development configuration for laptop testing
- `config_rpi.yaml` - Production configuration for Raspberry Pi
- `machine_files/stern_trident.yaml` - Hardware-specific switch/coil/light mappings
- `display_config.yaml` - Display and DMD configuration

## Development Workflow

### 1. Laptop Development
```bash
mpf -c config_dev.yaml
```

Uses virtual hardware for initial development and testing.

**Keyboard Controls:**
- `S` - Start button
- `Z` - Left flipper
- `/` - Right flipper
- `X` - Left slingshot
- `.` - Right slingshot
- `1,2,3` - Toggle trough switches

### 2. Raspberry Pi Deployment
```bash
mpf -c config_rpi.yaml
```

Connects to actual LISY hardware via USB serial connection.

## LISY Protocol Configuration

The RPU v102 board communicates using LISY protocol:
- **Serial Connection**: /dev/ttyUSB0 @ 115200 baud
- **Platform**: stern
- **Protocol Version**: 2
- **Display Support**: DMD via LISY

## Directory Structure

```
├── config.yaml              # Main configuration
├── config_dev.yaml          # Development config
├── config_rpi.yaml          # Production config
├── display_config.yaml      # Display settings
├── machine_files/
│   └── stern_trident.yaml   # Hardware mappings
├── modes/
│   ├── base/                # Base game mode
│   ├── attract/             # Attract mode
│   └── game/                # Main game mode
├── shows/                   # Light shows
├── sounds/                  # Sound files
├── images/                  # Image assets
└── logs/                    # Log files
```

## Next Steps

1. **Arduino Code**: Implement LISY protocol on RPU v102 board
2. **Hardware Mapping**: Adjust switch/coil numbers in stern_trident.yaml
3. **Game Logic**: Develop game-specific modes and rules
4. **Testing**: Validate on laptop before Pi deployment
5. **Display**: Configure specific display protocol for your setup

## Running the Project

**Development (Laptop):**
```bash
mpf -c config_dev.yaml
```

**Production (Raspberry Pi):**
```bash
mpf -c config_rpi.yaml
```

**Monitor Mode (for debugging):**
```bash
mpf monitor -c config_dev.yaml
```