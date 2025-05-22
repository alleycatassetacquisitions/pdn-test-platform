#!/usr/bin/env python3
"""
Tests for the SerialConnection class.
"""

import unittest
import os
import sys

# Add parent directory to path to make imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.serial_connection import SerialConnection, SerialConnectionError


class TestSerialConnection(unittest.TestCase):
    """Test cases for the SerialConnection class."""
    
    def test_list_ports(self):
        """Test listing available serial ports."""
        ports = SerialConnection.list_ports()
        self.assertIsInstance(ports, list)
        # We can't assert much more than this, as ports vary by system
    
    def test_init(self):
        """Test initialization of the SerialConnection class."""
        # Test with default values
        conn = SerialConnection()
        self.assertIsNone(conn.port)
        self.assertEqual(conn.baud_rate, 115200)
        self.assertEqual(conn.timeout, 1.0)
        self.assertEqual(conn.reconnect_attempts, 3)
        self.assertEqual(conn.reconnect_delay, 2.0)
        self.assertFalse(conn.connected)
        self.assertIsNone(conn.serial)
        
        # Test with custom values
        conn = SerialConnection(
            port="COM1",
            baud_rate=9600,
            timeout=0.5,
            reconnect_attempts=2,
            reconnect_delay=1.0
        )
        self.assertEqual(conn.port, "COM1")
        self.assertEqual(conn.baud_rate, 9600)
        self.assertEqual(conn.timeout, 0.5)
        self.assertEqual(conn.reconnect_attempts, 2)
        self.assertEqual(conn.reconnect_delay, 1.0)
    
    def test_connect_no_port(self):
        """Test connecting without specifying a port."""
        conn = SerialConnection()
        with self.assertRaises(SerialConnectionError):
            conn.connect()
    
    def test_disconnect_not_connected(self):
        """Test disconnecting when not connected."""
        conn = SerialConnection()
        self.assertFalse(conn.disconnect())
    
    def test_is_connected(self):
        """Test is_connected method."""
        conn = SerialConnection()
        self.assertFalse(conn.is_connected())


if __name__ == "__main__":
    unittest.main() 