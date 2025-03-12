from typing import Dict, Any, Optional, List, Union
import json
import logging
import time
import os
import requests
import base64
from pathlib import Path
from anus.tools.web3.nft_base_tool import NFTBaseTool
from anus.tools.base.tool_result import ToolResult

class NFTCreationTool(NFTBaseTool):
    """
    Tool for creating and minting NFTs on multiple blockchains.
    Supports metadata creation, asset upload, and mint operations.
    """
    name = "nft_creation"
    description = "Create and mint NFTs with metadata, image uploading, and attribute management"
    
    def __init__(self, 
                 rpc_url: str = "https://api.mainnet-beta.solana.com",
                 private_key_path: Optional[str] = None,
                 ipfs_upload_api: Optional[str] = None,
                 ipfs_api_key: Optional[str] = None,
                 temp_dir: str = "./temp",
                 **kwargs):
        super().__init__(rpc_url=rpc_url, private_key_path=private_key_path, **kwargs)
        
        # IPFS upload configuration
        self.ipfs_upload_api = ipfs_upload_api or "https://api.pinata.cloud/pinning/pinFileToIPFS"
        self.ipfs_api_key = ipfs_api_key
        
        # Temporary directory for file operations
        self.temp_dir = temp_dir
        os.makedirs(self.temp_dir, exist_ok=True)
    
    @property
    def parameters(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "create_metadata", "upload_image", "mint_nft", 
                        "create_collection", "add_to_collection", "update_metadata"
                    ],
                    "description": "The NFT creation action to perform"
                },
                "name": {
                    "type": "string",
                    "description": "Name of the NFT or collection"
                },
                "description": {
                    "type": "string",
                    "description": "Description of the NFT or collection"
                },
                "image_url": {
                    "type": "string",
                    "description": "URL to an image for the NFT or collection"
                },
                "image_data": {
                    "type": "string",
                    "description": "Base64-encoded image data for direct upload"
                },
                "attributes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "trait_type": {"type": "string"},
                            "value": {"type": "string"}
                        }
                    },
                    "description": "Array of attribute objects with trait_type and value properties"
                },
                "collection_address": {
                    "type": "string",
                    "description": "Address of the collection for the NFT"
                },
                "supply": {
                    "type": "integer",
                    "description": "Number of copies to mint (default: 1 for standard NFT)"
                },
                "creator_royalties": {
                    "type": "number",
                    "description": "Percentage of royalties for secondary sales (0-100)"
                },
                "external_url": {
                    "type": "string",
                    "description": "External URL for the NFT"
                },
                "blockchain": {
                    "type": "string",
                    "enum": ["solana", "ethereum", "polygon"],
                    "description": "Blockchain to mint the NFT on (default: solana)"
                },
                "metadata_uri": {
                    "type": "string",
                    "description": "URI to existing metadata for minting"
                },
                "recipient_address": {
                    "type": "string",
                    "description": "Recipient wallet address for the minted NFT"
                },
                "is_mutable": {
                    "type": "boolean",
                    "description": "Whether the NFT metadata can be changed after minting"
                },
                "category": {
                    "type": "string",
                    "description": "Category or type of the NFT (e.g., art, collectible, game)"
                }
            },
            "required": ["action"]
        }
    
    def execute(self, **kwargs) -> Union[Dict[str, Any], ToolResult]:
        """Execute the NFT creation tool with the given parameters"""
        action = kwargs.get("action")
        
        try:
            if action == "create_metadata":
                return self._create_metadata(
                    name=kwargs.get("name", ""),
                    description=kwargs.get("description", ""),
                    image_url=kwargs.get("image_url", ""),
                    attributes=kwargs.get("attributes", []),
                    external_url=kwargs.get("external_url", ""),
                    collection_address=kwargs.get("collection_address"),
                    category=kwargs.get("category", "")
                )
            elif action == "upload_image":
                return self._upload_image(
                    image_url=kwargs.get("image_url"),
                    image_data=kwargs.get("image_data")
                )
            elif action == "mint_nft":
                return self._mint_nft(
                    metadata_uri=kwargs.get("metadata_uri"),
                    recipient_address=kwargs.get("recipient_address"),
                    supply=kwargs.get("supply", 1),
                    blockchain=kwargs.get("blockchain", "solana"),
                    is_mutable=kwargs.get("is_mutable", True)
                )
            elif action == "create_collection":
                return self._create_collection(
                    name=kwargs.get("name", ""),
                    description=kwargs.get("description", ""),
                    image_url=kwargs.get("image_url", ""),
                    royalties=kwargs.get("creator_royalties", 5),
                    blockchain=kwargs.get("blockchain", "solana")
                )
            elif action == "add_to_collection":
                return self._add_to_collection(
                    nft_address=kwargs.get("nft_address"),
                    collection_address=kwargs.get("collection_address")
                )
            elif action == "update_metadata":
                return self._update_metadata(
                    nft_address=kwargs.get("nft_address"),
                    updates=kwargs
                )
            else:
                return ToolResult(
                    tool_name=self.name,
                    status="error",
                    error=f"Unknown NFT creation action: {action}"
                )
        except Exception as e:
            logging.error(f"Error executing NFT creation action {action}: {e}")
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Error executing NFT creation action {action}: {str(e)}"
            )
    
    def _create_metadata(self, name: str, description: str, image_url: str, 
                        attributes: List[Dict[str, str]] = None, external_url: str = "", 
                        collection_address: Optional[str] = None, category: str = "") -> ToolResult:
        """Create NFT metadata and return a JSON object"""
        if not name:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="NFT name is required"
            )
            
        # Build metadata following the Metaplex standard
        metadata = {
            "name": name,
            "description": description,
            "image": image_url,
            "attributes": attributes or [],
            "properties": {
                "files": [
                    {
                        "uri": image_url,
                        "type": self._guess_mime_type(image_url)
                    }
                ],
                "category": category or "image",
                "creators": [
                    {
                        "address": self._wallet_address or "WALLET_ADDRESS_REQUIRED",
                        "share": 100
                    }
                ]
            }
        }
        
        if external_url:
            metadata["external_url"] = external_url
            
        if collection_address:
            metadata["collection"] = {
                "name": name + " Collection",
                "family": name.replace(" ", "_").lower() + "_collection",
                "address": collection_address
            }
        
        # Generate temporary JSON file
        timestamp = int(time.time())
        json_path = os.path.join(self.temp_dir, f"metadata_{timestamp}.json")
        
        with open(json_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return ToolResult.success(
            tool_name=self.name,
            result={
                "metadata": metadata,
                "local_path": json_path,
                "message": "Metadata created successfully. Use upload_image to add an image, then mint_nft to mint."
            }
        )
    
    def _upload_image(self, image_url: Optional[str] = None, image_data: Optional[str] = None) -> ToolResult:
        """Upload an image to IPFS and return the IPFS URI"""
        if not self.ipfs_api_key:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="IPFS API key is required for image upload. Please set ipfs_api_key."
            )
            
        if not image_url and not image_data:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Either image_url or image_data is required"
            )
        
        try:
            # If image_url is provided, download the image first
            if image_url:
                timestamp = int(time.time())
                extension = self._get_extension_from_url(image_url)
                local_path = os.path.join(self.temp_dir, f"image_{timestamp}{extension}")
                
                response = requests.get(image_url, stream=True, timeout=10)
                response.raise_for_status()
                
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            # If image_data is provided (base64), decode and save it
            elif image_data:
                try:
                    timestamp = int(time.time())
                    # Try to determine image format from base64 data
                    if image_data.startswith("data:image/"):
                        # Extract mime type and data
                        mime_format = image_data.split(";")[0].split("/")[1]
                        extension = f".{mime_format}"
                        # Remove the data URL prefix
                        image_data = image_data.split(",")[1]
                    else:
                        # Default to PNG if format not detected
                        extension = ".png"
                    
                    local_path = os.path.join(self.temp_dir, f"image_{timestamp}{extension}")
                    
                    image_bytes = base64.b64decode(image_data)
                    with open(local_path, 'wb') as f:
                        f.write(image_bytes)
                except Exception as e:
                    return ToolResult(
                        tool_name=self.name,
                        status="error",
                        error=f"Error decoding base64 image data: {str(e)}"
                    )
            
            # Upload to IPFS
            headers = {
                "Authorization": f"Bearer {self.ipfs_api_key}"
            }
            
            with open(local_path, 'rb') as f:
                files = {
                    'file': (os.path.basename(local_path), f)
                }
                
                response = requests.post(
                    self.ipfs_upload_api,
                    headers=headers,
                    files=files,
                    timeout=30
                )
                
                response.raise_for_status()
                result = response.json()
                
                if 'IpfsHash' in result:
                    ipfs_hash = result['IpfsHash']
                    ipfs_uri = f"ipfs://{ipfs_hash}"
                    http_url = self.resolve_ipfs_url(ipfs_uri)
                    
                    return ToolResult.success(
                        tool_name=self.name,
                        result={
                            "ipfs_uri": ipfs_uri,
                            "http_url": http_url,
                            "ipfs_hash": ipfs_hash,
                            "local_path": local_path
                        }
                    )
                else:
                    return ToolResult(
                        tool_name=self.name,
                        status="error",
                        error=f"IPFS upload failed: {result}"
                    )
                    
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Error uploading image: {str(e)}"
            )
    
    def _mint_nft(self, metadata_uri: str, recipient_address: Optional[str] = None, 
                 supply: int = 1, blockchain: str = "solana", is_mutable: bool = True) -> ToolResult:
        """Mint an NFT on the specified blockchain"""
        if not self._keypair:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Private key not loaded. Please load a wallet first."
            )
            
        if not metadata_uri:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Metadata URI is required"
            )
        
        # For Solana NFTs
        if blockchain.lower() == "solana":
            try:
                # If metadata_uri is a local file, upload it to IPFS first
                if os.path.isfile(metadata_uri):
                    # Read the metadata file
                    with open(metadata_uri, 'r') as f:
                        metadata = json.load(f)
                    
                    # Upload metadata to IPFS
                    if self.ipfs_api_key:
                        headers = {
                            "Authorization": f"Bearer {self.ipfs_api_key}"
                        }
                        
                        files = {
                            'file': (os.path.basename(metadata_uri), open(metadata_uri, 'rb'))
                        }
                        
                        response = requests.post(
                            self.ipfs_upload_api,
                            headers=headers,
                            files=files,
                            timeout=30
                        )
                        
                        response.raise_for_status()
                        result = response.json()
                        
                        if 'IpfsHash' in result:
                            ipfs_hash = result['IpfsHash']
                            metadata_uri = f"ipfs://{ipfs_hash}"
                        else:
                            return ToolResult(
                                tool_name=self.name,
                                status="error",
                                error=f"Metadata upload to IPFS failed: {result}"
                            )
                    else:
                        return ToolResult(
                            tool_name=self.name,
                            status="error",
                            error="IPFS API key is required for metadata upload"
                        )
                
                # Create NFT mint account
                from solana.keypair import Keypair
                from solana.publickey import PublicKey
                from solana.transaction import Transaction
                from solana.system_program import CreateAccountParams, create_account
                from spl.token.instructions import create_mint
                from spl.token.constants import TOKEN_PROGRAM_ID
                from metaplex.transactions import create_metadata_instruction
                
                # Create a new keypair for the NFT
                mint_keypair = Keypair()
                
                # First create a token mint account
                resp = self._client.get_minimum_balance_for_rent_exemption(82)
                lamports = resp["result"]
                
                # Create system account for token mint
                create_account_ix = create_account(
                    CreateAccountParams(
                        from_pubkey=self._keypair.public_key,
                        new_account_pubkey=mint_keypair.public_key,
                        lamports=lamports,
                        space=82,
                        program_id=TOKEN_PROGRAM_ID
                    )
                )
                
                # Create mint instruction
                create_mint_ix = create_mint(
                    program_id=TOKEN_PROGRAM_ID,
                    mint=mint_keypair.public_key,
                    mint_authority=self._keypair.public_key,
                    freeze_authority=self._keypair.public_key,
                    decimals=0  # NFTs have 0 decimals
                )
                
                # Create metadata instruction
                recipient = recipient_address if recipient_address else str(self._keypair.public_key)
                metadata_args = {
                    "name": "",  # Will be filled from URI
                    "symbol": "",  # Will be filled from URI
                    "uri": metadata_uri,
                    "creators": [
                        {
                            "address": str(self._keypair.public_key),
                            "verified": True,
                            "share": 100
                        }
                    ],
                    "seller_fee_basis_points": 0,  # No royalties by default
                    "is_mutable": is_mutable
                }
                
                create_metadata_ix = create_metadata_instruction(
                    mint=mint_keypair.public_key,
                    metadata_args=metadata_args,
                    update_authority=self._keypair.public_key,
                    payer=self._keypair.public_key
                )
                
                # Create transaction with both instructions
                transaction = Transaction().add(
                    create_account_ix, create_mint_ix, create_metadata_ix
                )
                
                # Sign and send transaction
                transaction_signature = self._client.send_transaction(
                    transaction, self._keypair, mint_keypair
                )
                
                if "result" in transaction_signature:
                    tx_id = transaction_signature["result"]
                    
                    return ToolResult.success(
                        tool_name=self.name,
                        result={
                            "transaction_signature": tx_id,
                            "nft_address": str(mint_keypair.public_key),
                            "metadata_uri": metadata_uri,
                            "owner": recipient,
                            "blockchain": "solana",
                            "is_mutable": is_mutable,
                            "status": "minted"
                        }
                    )
                else:
                    return ToolResult(
                        tool_name=self.name,
                        status="error",
                        error=f"Failed to mint NFT: {transaction_signature.get('error', 'Unknown error')}"
                    )
                    
            except ImportError:
                return ToolResult(
                    tool_name=self.name,
                    status="error",
                    error="Required packages not installed. Please install solana, spl, and metaplex packages."
                )
            except Exception as e:
                return ToolResult(
                    tool_name=self.name,
                    status="error",
                    error=f"Error minting Solana NFT: {str(e)}"
                )
                
        elif blockchain.lower() in ["ethereum", "polygon"]:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Minting on {blockchain} is not implemented yet. Only Solana is currently supported."
            )
        else:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Unsupported blockchain: {blockchain}"
            )
    
    def _create_collection(self, name: str, description: str, image_url: str, 
                         royalties: float = 5.0, blockchain: str = "solana") -> ToolResult:
        """Create an NFT collection"""
        # For collection creation, we use a similar process to NFT minting
        # but with special collection attributes
        
        # Create metadata for the collection
        collection_metadata = {
            "name": name,
            "description": description,
            "image": image_url,
            "attributes": [],
            "properties": {
                "files": [
                    {
                        "uri": image_url,
                        "type": self._guess_mime_type(image_url)
                    }
                ],
                "category": "collection",
                "creators": [
                    {
                        "address": self._wallet_address or "WALLET_ADDRESS_REQUIRED",
                        "share": 100
                    }
                ]
            },
            "seller_fee_basis_points": int(royalties * 100),  # Convert percentage to basis points
            "is_collection": True
        }
        
        # Generate temporary JSON file
        timestamp = int(time.time())
        json_path = os.path.join(self.temp_dir, f"collection_{timestamp}.json")
        
        with open(json_path, 'w') as f:
            json.dump(collection_metadata, f, indent=2)
        
        # For Solana, we need to first upload the metadata and then mint the collection NFT
        if blockchain.lower() == "solana":
            # Upload metadata if IPFS key is available
            if self.ipfs_api_key:
                # Code to upload metadata to IPFS
                headers = {
                    "Authorization": f"Bearer {self.ipfs_api_key}"
                }
                
                files = {
                    'file': (os.path.basename(json_path), open(json_path, 'rb'))
                }
                
                try:
                    response = requests.post(
                        self.ipfs_upload_api,
                        headers=headers,
                        files=files,
                        timeout=30
                    )
                    
                    response.raise_for_status()
                    result = response.json()
                    
                    if 'IpfsHash' in result:
                        ipfs_hash = result['IpfsHash']
                        metadata_uri = f"ipfs://{ipfs_hash}"
                        
                        # Now mint the collection as an NFT
                        mint_result = self._mint_nft(
                            metadata_uri=metadata_uri,
                            recipient_address=None,  # Use default (minter)
                            supply=1,
                            blockchain=blockchain,
                            is_mutable=True  # Collections are typically mutable
                        )
                        
                        if mint_result.status == "success":
                            # Add collection-specific information to the result
                            result_data = mint_result.result
                            result_data["collection_name"] = name
                            result_data["collection_description"] = description
                            result_data["royalties"] = royalties
                            result_data["type"] = "collection"
                            
                            return ToolResult.success(
                                tool_name=self.name,
                                result=result_data
                            )
                        else:
                            return mint_result  # Return the error from minting
                    else:
                        return ToolResult(
                            tool_name=self.name,
                            status="error",
                            error=f"Metadata upload to IPFS failed: {result}"
                        )
                except Exception as e:
                    return ToolResult(
                        tool_name=self.name,
                        status="error",
                        error=f"Error creating collection: {str(e)}"
                    )
            else:
                return ToolResult(
                    tool_name=self.name,
                    status="error",
                    error="IPFS API key is required for collection creation"
                )
        else:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Collection creation on {blockchain} is not implemented yet"
            )
    
    def _add_to_collection(self, nft_address: str, collection_address: str) -> ToolResult:
        """Add an NFT to a collection"""
        if not self._keypair:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Private key not loaded. Please load a wallet first."
            )
            
        if not nft_address or not collection_address:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="NFT address and collection address are required"
            )
        
        # This is a placeholder for the actual implementation
        return ToolResult(
            tool_name=self.name,
            status="error",
            error="Collection management is not fully implemented yet"
        )
    
    def _update_metadata(self, nft_address: str, updates: Dict[str, Any]) -> ToolResult:
        