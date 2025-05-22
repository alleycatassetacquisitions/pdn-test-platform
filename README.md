# Serial Log Testing Platform

A comprehensive platform for testing and analyzing serial log data from embedded devices.

## Overview

This platform provides tools for connecting to serial devices, capturing log data, processing and analyzing logs, and running automated tests. It is designed to work with multiple device types, including MKR and ESP32 boards.

## Features

- Serial device connection and management
- Automated log collection and parsing
- Device-specific log interpretation
- Test automation framework
- Reporting and visualization tools

## Project Structure

```
pdn-test-platform/
├── config/             # Configuration files
├── data/               # Data storage
├── src/                # Source code
│   ├── core/           # Core functionality
│   ├── devices/        # Device-specific implementations
│   ├── logs/           # Log processing modules
│   ├── tests/          # Testing framework
│   └── ui/             # User interface components
```

## Getting Started

1. Clone the repository
2. Install the dependencies: `pip install -r requirements.txt`
3. Configure your devices in the config directory
4. Run the platform: `python -m src.main`

## Requirements

See `requirements.txt` for Python package dependencies. 