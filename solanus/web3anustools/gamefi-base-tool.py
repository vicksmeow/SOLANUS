from typing import Dict, Any, Optional, List, Union
import json
import logging
import requests
import time
from anus.tools.base.tool import BaseTool
from anus.tools.base.tool_result import ToolResult

class GameFiBaseTool(BaseTool):
    """
    Base class for GameFi integration tools.
    Provides common functionality for blockchain gaming tools.
    """
    name = "gamefi_base"
    description = "Base class for GameFi tools. Not meant to be used directly."
    
    def __init__(self, 
                 rpc_url: str = "https://api.mainnet-beta.solana.com",
                 private_key_path: Optional[str] = None,
                 game_api_keys: Optional[Dict[str, str]] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.rpc_url = rpc_url
        self.private_key_path = private_key_path
        self.game_api_keys = game_api_keys or {}
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
            raise ImportError("Solana package required for GameFi tools. Install with 'pip install solana'")
    
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
    
    def api_request(self, endpoint: str, method: str = "GET", params: Optional[Dict[str, Any]] = None, 
                 headers: Optional[Dict[str, str]] = None, game_id: Optional[str] = None) -> Dict[str, Any]:
        """Make a request to a game API"""
        headers = headers or {}
        
        # Add API key if available for the specified game
        if game_id and game_id in self.game_api_keys:
            headers["Authorization"] = f"Bearer {self.game_api_keys[game_id]}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(endpoint, params=params, headers=headers, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(endpoint, json=params, headers=headers, timeout=10)
            else:
                return {"error": f"Unsupported HTTP method: {method}"}
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"API request error for {endpoint}: {e}")
            return {"error": str(e)}
    
    def _simulate_game_api_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate a game API response for demonstration purposes"""
        return {
            "success": True,
            "timestamp": int(time.time()),
            "data": data
        }
