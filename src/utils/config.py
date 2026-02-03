"""
Configuration Management

Loads and manages configuration from files and environment variables.
Centralizes config for all components.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Central configuration manager for CuratAI.
    
    Loads configuration from:
    - Environment variables (highest priority)
    - config.json files
    - Defaults
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir) if config_dir else Path(__file__).parent.parent.parent / "config"
        self.config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from multiple sources"""
        # Start with defaults
        self.config = self._get_defaults()
        
        # Override with config file if exists
        config_file = self.config_dir / "config.json"
        if config_file.exists():
            with open(config_file) as f:
                file_config = json.load(f)
                self.config.update(file_config)
                logger.info(f"Loaded config from {config_file}")
        
        # Override with environment variables
        self._load_env_vars()
    
    def _get_defaults(self) -> Dict[str, Any]:
        """Default configuration"""
        return {
            "debug": False,
            "log_level": "INFO",
            "opik": {
                "enabled": True,
                "api_key": "",
                "workspace": "curatai-workspace",
                "project": "curatai-core"
            },
            "web3": {
                "enabled": True,
                "ipfs_gateway": "https://gateway.pinata.cloud",
                "did_method": "key"
            },
            "llm": {
                "provider": "openai",
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 2000
            },
            "database": {
                "type": "sqlite",
                "path": ":memory:"
            }
        }
    
    def _load_env_vars(self):
        """Load configuration from environment variables"""
        env_mappings = {
            "CURATAΙ_DEBUG": ("debug", self._parse_bool),
            "CURATAΙ_LOG_LEVEL": ("log_level", str),
            "OPIK_API_KEY": ("opik.api_key", str),
            "OPIK_WORKSPACE": ("opik.workspace", str),
            "LLM_PROVIDER": ("llm.provider", str),
            "LLM_MODEL": ("llm.model", str),
        }
        
        for env_var, (config_path, parser) in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                self._set_nested(config_path, parser(value))
                logger.debug(f"Loaded {env_var} from environment")
    
    def _set_nested(self, path: str, value: Any):
        """Set nested config value using dot notation"""
        keys = path.split(".")
        config = self.config
        for key in keys[:-1]:
            config = config.setdefault(key, {})
        config[keys[-1]] = value
    
    def _parse_bool(self, value: str) -> bool:
        """Parse boolean from string"""
        return value.lower() in ("true", "1", "yes", "on")
    
    def get(self, path: str, default: Any = None) -> Any:
        """
        Get config value using dot notation.
        
        Example: config.get("opik.api_key")
        """
        keys = path.split(".")
        value = self.config
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
            
            if value is None:
                return default
        
        return value
    
    def get_config_dict(self) -> Dict[str, Any]:
        """Get entire config as dictionary"""
        return self.config.copy()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    config = ConfigManager()
    
    print("\n=== Configuration ===\n")
    print(f"Debug: {config.get('debug')}")
    print(f"Log Level: {config.get('log_level')}")
    print(f"Opik Workspace: {config.get('opik.workspace')}")
    print(f"LLM Provider: {config.get('llm.provider')}")
    print(f"LLM Model: {config.get('llm.model')}")
