#!/usr/bin/env python3
"""
Serial connection module for the Serial Log Testing Platform.
Provides basic functionality for connecting to and managing serial devices.
"""

import logging
import time
import serial
import serial.tools.list_ports
from typing import List, Optional, Dict, Any, Tuple


class SerialConnectionError(Exception):
    """Exception raised for errors in the SerialConnection class."""
    pass


class SerialConnection:
    """Class for managing serial connections to devices."""
    
    def __init__(self, port: Optional[str] = None, baud_rate: int = 115200, 
                 timeout: float = 1.0, reconnect_attempts: int = 3, 
                 reconnect_delay: float = 2.0):
        """
        Initialize a serial connection.
        
        Args:
            port: The serial port to connect to. If None, no connection is made.
            baud_rate: The baud rate for the connection.
            timeout: Read timeout in seconds.
            reconnect_attempts: Number of reconnection attempts before giving up.
            reconnect_delay: Delay between reconnection attempts in seconds.
        """
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.reconnect_attempts = reconnect_attempts
        self.reconnect_delay = reconnect_delay
        self.serial = None
        self.connected = False
        self.logger = logging.getLogger(__name__)
    
    def connect(self, port: Optional[str] = None) -> bool:
        """
        Connect to the specified serial port.
        
        Args:
            port: The serial port to connect to. If None, use the port from initialization.
            
        Returns:
            bool: True if connection successful, False otherwise.
            
        Raises:
            SerialConnectionError: If connection fails after reconnect attempts.
        """
        if port:
            self.port = port
            
        if not self.port:
            self.logger.error("No port specified for connection")
            raise SerialConnectionError("No port specified for connection")
            
        self.logger.info(f"Connecting to port {self.port} at {self.baud_rate} baud")
        
        for attempt in range(self.reconnect_attempts):
            try:
                self.serial = serial.Serial(
                    port=self.port,
                    baudrate=self.baud_rate,
                    timeout=self.timeout
                )
                self.connected = True
                self.logger.info(f"Successfully connected to {self.port}")
                return True
            except serial.SerialException as e:
                self.logger.warning(f"Connection attempt {attempt + 1}/{self.reconnect_attempts} failed: {str(e)}")
                if attempt < self.reconnect_attempts - 1:
                    time.sleep(self.reconnect_delay)
        
        self.logger.error(f"Failed to connect to {self.port} after {self.reconnect_attempts} attempts")
        raise SerialConnectionError(f"Failed to connect to {self.port} after {self.reconnect_attempts} attempts")
    
    def disconnect(self) -> bool:
        """
        Disconnect from the serial port.
        
        Returns:
            bool: True if disconnection successful, False otherwise.
        """
        if not self.connected or not self.serial:
            self.logger.warning("Not connected, nothing to disconnect")
            return False
            
        try:
            self.serial.close()
            self.connected = False
            self.logger.info(f"Disconnected from {self.port}")
            return True
        except serial.SerialException as e:
            self.logger.error(f"Error disconnecting from {self.port}: {str(e)}")
            return False
    
    def is_connected(self) -> bool:
        """
        Check if the serial connection is active.
        
        Returns:
            bool: True if connected, False otherwise.
        """
        return self.connected and self.serial and self.serial.is_open
    
    @staticmethod
    def list_ports() -> List[Dict[str, Any]]:
        """
        List all available serial ports.
        
        Returns:
            List[Dict[str, Any]]: List of dictionaries with port information.
        """
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append({
                'device': port.device,
                'name': port.name,
                'description': port.description,
                'hwid': port.hwid,
                'vid': port.vid,
                'pid': port.pid,
                'serial_number': port.serial_number,
                'location': port.location,
                'manufacturer': port.manufacturer,
                'product': port.product,
                'interface': port.interface
            })
        return ports
    
    @staticmethod
    def find_port_by_vid_pid(vid: int, pid: Optional[int] = None) -> Optional[str]:
        """
        Find a port by Vendor ID and optionally Product ID.
        
        Args:
            vid: Vendor ID
            pid: Product ID (optional)
            
        Returns:
            Optional[str]: Port name if found, None otherwise.
        """
        for port in serial.tools.list_ports.comports():
            if port.vid == vid and (pid is None or port.pid == pid):
                return port.device
        return None
    
    def read(self, size: int = 1) -> bytes:
        """
        Read data from the serial port.
        
        Args:
            size: Number of bytes to read.
            
        Returns:
            bytes: Data read from the port.
            
        Raises:
            SerialConnectionError: If not connected or read error occurs.
        """
        if not self.is_connected():
            self.logger.error("Cannot read: not connected")
            raise SerialConnectionError("Cannot read: not connected")
            
        try:
            data = self.serial.read(size)
            return data
        except serial.SerialException as e:
            self.logger.error(f"Error reading from {self.port}: {str(e)}")
            raise SerialConnectionError(f"Error reading from {self.port}: {str(e)}")
    
    def write(self, data: bytes) -> int:
        """
        Write data to the serial port.
        
        Args:
            data: Data to write.
            
        Returns:
            int: Number of bytes written.
            
        Raises:
            SerialConnectionError: If not connected or write error occurs.
        """
        if not self.is_connected():
            self.logger.error("Cannot write: not connected")
            raise SerialConnectionError("Cannot write: not connected")
            
        try:
            return self.serial.write(data)
        except serial.SerialException as e:
            self.logger.error(f"Error writing to {self.port}: {str(e)}")
            raise SerialConnectionError(f"Error writing to {self.port}: {str(e)}") 