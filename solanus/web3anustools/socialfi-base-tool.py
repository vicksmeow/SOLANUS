from typing import Dict, Any, Optional, List, Union
import json
import logging
import requests
import time
from datetime import datetime
from anus.tools.base.tool import BaseTool
from anus.tools.base.tool_result import ToolResult

class SocialFiBaseTool(BaseTool):
    """
    Base class for SocialFi integration tools.
    Provides common functionality for social token and community tools.
    """
    name = "socialfi_base"
    description = "Base class for SocialFi tools. Not meant to be used directly."
    
    def __init__(self, 
                 rpc_url: str = "https://api.mainnet-beta.solana.com",
                 private_key_path: Optional[str] = None,
                 indexer_api_key: Optional[str] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.rpc_url = rpc_url
        self.private_key_path = private_key_path
        self.indexer_api_key = indexer_api_key
        self._client = None
        self._keypair = None
        self._wallet_address = None
        
        # Initialize blockchain client
        self._initialize_client()
        
        # Load wallet if private key is provided
        if private_key_path:
            self._load_wallet()
    
    def _initialize_client(self):
        """Initialize blockchain client"""
        try:
            # We're using dynamic imports to handle optional dependencies
            from solana.rpc.api import Client
            self._client = Client(self.rpc_url)
            logging.info(f"Solana client initialized with RPC URL: {self.rpc_url}")
        except ImportError:
            logging.error("Solana package not installed. Please install with 'pip install solana'")
            raise ImportError("Solana package required for SocialFi tools. Install with 'pip install solana'")
    
    def _load_wallet(self):
        """Load wallet from private key file"""
        try:
            from solana.keypair import Keypair
            
            try:
                with open(self.private_key_path, 'r') as f:
                    private_key_json = json.load(f)
                    private_key_bytes = bytes(private_key_json)
                    self._keypair = Keypair.from_secret_key(private_key_bytes)
                    self._wallet_address = str(self._keypair.public_key)
                    logging.info(f"Wallet loaded with address: {self._wallet_address}")
            except Exception as e:
                logging.error(f"Error loading wallet: {e}")
                raise ValueError(f"Failed to load wallet from {self.private_key_path}: {e}")
        except ImportError:
            logging.error("Solana package not installed. Please install with 'pip install solana'")
            raise ImportError("Solana package required for wallet functionality")
    
    def fetch_json(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Fetch JSON data from a URL"""
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Error fetching JSON from {url}: {e}")
            return {}
    
    def post_json(self, url: str, data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Post JSON data to a URL"""
        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Error posting JSON to {url}: {e}")
            return {}
    
    def format_timestamp(self, timestamp: Optional[float] = None) -> str:
        """Format a timestamp as ISO 8601 string"""
        if timestamp is None:
            timestamp = time.time()
        return datetime.fromtimestamp(timestamp).isoformat()
    
    def is_valid_address(self, address: str, blockchain: str = "solana") -> bool:
        """Check if an address is valid for the specified blockchain"""
        if not address:
            return False
            
        if blockchain.lower() == "solana":
            # Simple Solana address validation (base58 encoding, correct length)
            import base58
            try:
                decoded = base58.b58decode(address)
                return len(decoded) == 32
            except:
                return False
        elif blockchain.lower() in ["ethereum", "polygon"]:
            # Simple Ethereum address validation (0x prefix, hex string, correct length)
            if address.startswith("0x") and len(address) == 42:
                try:
                    int(address[2:], 16)  # Check if hex string
                    return True
                except:
                    return False
            return False
        else:
            return False
    
    def _simulate_api_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate an API response with standard metadata"""
        return {
            "success": True,
            "timestamp": self.format_timestamp(),
            "data": data
        }
