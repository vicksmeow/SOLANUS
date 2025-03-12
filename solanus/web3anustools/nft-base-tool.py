from typing import Dict, Any, Optional, List, Union
import json
import logging
import time
from anus.tools.base.tool import BaseTool
from anus.tools.base.tool_result import ToolResult

class NFTBaseTool(BaseTool):
    """
    Base class for NFT-related tools.
    Provides common functionality for NFT tools.
    """
    name = "nft_base"
    description = "Base class for NFT tools. Not meant to be used directly."
    
    def __init__(self, 
                 rpc_url: str = "https://api.mainnet-beta.solana.com",
                 private_key_path: Optional[str] = None,
                 ipfs_gateway: str = "https://ipfs.io/ipfs/",
                 arweave_gateway: str = "https://arweave.net/",
                 **kwargs):
        super().__init__(**kwargs)
        self.rpc_url = rpc_url
        self.private_key_path = private_key_path
        self.ipfs_gateway = ipfs_gateway
        self.arweave_gateway = arweave_gateway
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
            raise ImportError("Solana package required for NFT tools. Install with 'pip install solana'")
    
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
    
    def resolve_ipfs_url(self, ipfs_uri: str) -> str:
        """Convert IPFS URI to HTTP URL using configured gateway"""
        if not ipfs_uri:
            return ""
            
        # Handle various IPFS URI formats
        if ipfs_uri.startswith("ipfs://"):
            ipfs_hash = ipfs_uri[7:]
            return f"{self.ipfs_gateway}{ipfs_hash}"
        elif ipfs_uri.startswith("ipfs/"):
            ipfs_hash = ipfs_uri[5:]
            return f"{self.ipfs_gateway}{ipfs_hash}"
        elif ipfs_uri.startswith("ipfs:"):
            ipfs_hash = ipfs_uri[5:]
            return f"{self.ipfs_gateway}{ipfs_hash}"
        # Already in HTTP format or other type of URI
        return ipfs_uri
    
    def resolve_arweave_url(self, arweave_uri: str) -> str:
        """Convert Arweave URI to HTTP URL using configured gateway"""
        if not arweave_uri:
            return ""
            
        # Handle various Arweave URI formats
        if arweave_uri.startswith("ar://"):
            ar_hash = arweave_uri[5:]
            return f"{self.arweave_gateway}{ar_hash}"
        elif arweave_uri.startswith("ar/"):
            ar_hash = arweave_uri[3:]
            return f"{self.arweave_gateway}{ar_hash}"
        elif arweave_uri.startswith("ar:"):
            ar_hash = arweave_uri[3:]
            return f"{self.arweave_gateway}{ar_hash}"
        # Already in HTTP format or other type of URI
        return arweave_uri
    
    def resolve_metadata_uri(self, uri: str) -> str:
        """Resolve a URI to an HTTP URL based on its protocol"""
        if not uri:
            return ""
            
        if uri.startswith(("ipfs://", "ipfs/", "ipfs:")):
            return self.resolve_ipfs_url(uri)
        elif uri.startswith(("ar://", "ar/", "ar:")):
            return self.resolve_arweave_url(uri)
        
        # Already HTTP URL or other protocol
        return uri
    
    def fetch_json(self, url: str) -> Dict[str, Any]:
        """Fetch JSON data from a URL"""
        import requests
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Error fetching JSON from {url}: {e}")
            return {}
    
    def fetch_metadata(self, metadata_uri: str) -> Dict[str, Any]:
        """Fetch and return NFT metadata from URI"""
        resolved_uri = self.resolve_metadata_uri(metadata_uri)
        return self.fetch_json(resolved_uri)
