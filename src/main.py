#!/usr/bin/env python3
"""
Main entry point for the Serial Log Testing Platform.
"""

import logging
import sys
import os
import argparse
import platform
import importlib
from src.core.config import Config
from src.core.serial_connection import SerialConnection, SerialConnectionError

# Check if required packages are installed
def check_dependencies():
    """Check if all required dependencies are installed."""
    missing_deps = []
    
    try:
        importlib.import_module('serial')
        importlib.import_module('serial.tools.list_ports')
    except ImportError:
        missing_deps.append('pyserial')
    
    try:
        importlib.import_module('yaml')
    except ImportError:
        missing_deps.append('pyyaml')
    
    if missing_deps:
        print("ERROR: Missing required dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nPlease install them using:")
        print("  pip install " + " ".join(missing_deps))
        sys.exit(1)

# Import remaining modules after dependency check
check_dependencies()

# Check if running in WSL
def is_wsl():
    """Check if running in Windows Subsystem for Linux."""
    if platform.system() == "Linux":
        try:
            with open('/proc/version', 'r') as f:
                if 'microsoft' in f.read().lower():
                    return True
        except:
            pass
    return False

# Setup logging
def setup_logging(log_level=logging.INFO):
    """Configure the logging system."""
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, 'platform.log')
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger('platform')

def list_available_ports():
    """List all available serial ports."""
    # Check if running in WSL and warn about port access
    if is_wsl():
        print("\nWARNING: You are running in Windows Subsystem for Linux (WSL).")
        print("Serial ports from Windows may not be directly accessible.")
        print("Consider running this tool directly in Windows or using usbipd-win to connect USB devices to WSL.")
        print("See: https://github.com/dorssel/usbipd-win\n")
    
    ports = SerialConnection.list_ports()
    
    if not ports:
        print("No serial ports found.")
        return
    
    print("Available serial ports:")
    for i, port in enumerate(ports):
        vid_pid = ""
        if port['vid'] is not None:
            vid_pid = f" [VID:{port['vid']:04X}"
            if port['pid'] is not None:
                vid_pid += f", PID:{port['pid']:04X}"
            vid_pid += "]"
            
        print(f"{i+1}. {port['device']} - {port['description']}{vid_pid}")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Serial Log Testing Platform')
    parser.add_argument('--config', '-c', help='Path to configuration file')
    parser.add_argument('--port', '-p', help='Serial port to connect to')
    parser.add_argument('--baud', '-b', type=int, help='Baud rate for serial connection')
    parser.add_argument('--list-ports', '-l', action='store_true', help='List available serial ports')
    parser.add_argument('--device', '-d', help='Device type (e.g., mkr, esp32)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    return parser.parse_args()

def main():
    """Main entry point for the application."""
    args = parse_arguments()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logging(log_level)
    logger.info("Starting Serial Log Testing Platform")
    
    # List ports if requested
    if args.list_ports:
        list_available_ports()
        return
    
    try:
        # Load configuration
        config = Config(args.config)
        logger.info("Configuration loaded successfully")
        
        # Get serial settings
        serial_config = config.get_serial_config()
        baud_rate = args.baud or serial_config.get('default_baud_rate', 115200)
        timeout = serial_config.get('timeout', 1.0)
        reconnect_attempts = serial_config.get('reconnect_attempts', 3)
        reconnect_delay = serial_config.get('reconnect_delay', 2.0)
        
        # If device specified, get its configuration
        port = args.port
        if args.device and not port:
            try:
                device_config = config.get_device_config(args.device)
                vendor_id = int(device_config.get('vendor_id', '0'), 0)  # Convert from hex string if needed
                device_baud = device_config.get('baud_rate', baud_rate)
                
                # Try to find port by vendor ID
                port = SerialConnection.find_port_by_vid_pid(vendor_id)
                if port:
                    logger.info(f"Found {args.device} device at port {port}")
                    baud_rate = device_baud
                else:
                    logger.warning(f"No {args.device} device found")
            except Exception as e:
                logger.error(f"Error getting device configuration: {str(e)}")
        
        # If no port specified or found, list available ports and exit
        if not port:
            logger.info("No port specified, listing available ports")
            list_available_ports()
            return
        
        # Create and connect serial connection
        serial_conn = SerialConnection(
            port=port,
            baud_rate=baud_rate,
            timeout=timeout,
            reconnect_attempts=reconnect_attempts,
            reconnect_delay=reconnect_delay
        )
        
        try:
            serial_conn.connect()
            logger.info(f"Connected to {port} at {baud_rate} baud")
            
            # Here you would typically start your application logic
            # For now, we'll just demonstrate reading some data
            
            print(f"Connected to {port}. Press Ctrl+C to exit.")
            print("Waiting for data...")
            
            try:
                while True:
                    if serial_conn.is_connected():
                        data = serial_conn.read(100)
                        if data:
                            # Decode bytes to string, replacing invalid characters
                            text = data.decode('utf-8', errors='replace')
                            print(text, end='', flush=True)
                    else:
                        logger.error("Connection lost")
                        break
            except KeyboardInterrupt:
                logger.info("Interrupted by user")
            finally:
                serial_conn.disconnect()
                logger.info("Disconnected from serial port")
            
        except SerialConnectionError as e:
            logger.error(f"Connection error: {str(e)}")
    
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
    
    logger.info("Serial Log Testing Platform stopped")

if __name__ == "__main__":
    main() 