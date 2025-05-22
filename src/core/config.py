#!/usr/bin/env python3
"""
Configuration module for the Serial Log Testing Platform.
Handles loading and managing configuration settings.
"""

import os
import logging
import yaml
from typing import Dict, Any, Optional


class ConfigError(Exception):
    """Exception raised for errors in the configuration module."""
    pass


class Config:
    """Class for managing configuration settings."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the configuration file. If None, use the default config.
        """
        self.logger = logging.getLogger(__name__)
        self.config_data = {}
        
        if config_path is None:
            # Use default config path
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            config_path = os.path.join(base_dir, 'config', 'default.yaml')
        
        self.config_path = config_path
        self.load_config()
    
    def load_config(self) -> None:
        """
        Load configuration from the config file.
        
        Raises:
            ConfigError: If loading fails.
        """
        try:
            with open(self.config_path, 'r') as file:
                self.config_data = yaml.safe_load(file)
                self.logger.info(f"Loaded configuration from {self.config_path}")
        except (IOError, yaml.YAMLError) as e:
            self.logger.error(f"Failed to load configuration from {self.config_path}: {str(e)}")
            raise ConfigError(f"Failed to load configuration from {self.config_path}: {str(e)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Dot-separated key path (e.g., 'serial.baud_rate')
            default: Default value to return if key is not found
            
        Returns:
            Any: The configuration value or default
        """
        keys = key.split('.')
        value = self.config_data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                self.logger.debug(f"Configuration key '{key}' not found, returning default value")
                return default
                
        return value
    
    def get_serial_config(self) -> Dict[str, Any]:
        """
        Get the serial connection configuration.
        
        Returns:
            Dict[str, Any]: Serial connection configuration
        """
        return self.get('serial', {})
    
    def get_device_config(self, device_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific device.
        
        Args:
            device_name: Name of the device
            
        Returns:
            Dict[str, Any]: Device configuration
            
        Raises:
            ConfigError: If device configuration not found
        """
        devices = self.get('devices', {})
        if device_name not in devices:
            self.logger.error(f"Device configuration for '{device_name}' not found")
            raise ConfigError(f"Device configuration for '{device_name}' not found")
            
        return devices[device_name] 