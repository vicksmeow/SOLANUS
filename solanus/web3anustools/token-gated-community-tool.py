from typing import Dict, Any, Optional, List, Union
import json
import logging
import time
import hashlib
import base64
from datetime import datetime, timedelta
from anus.tools.web3.socialfi_base_tool import SocialFiBaseTool
from anus.tools.base.tool_result import ToolResult

class TokenGatedCommunityTool(SocialFiBaseTool):
    """
    Tool for managing token-gated communities and access control.
    Provides functionality for creating, configuring, and verifying access to token-gated spaces.
    """
    name = "token_gated_community"
    description = "Manage token-gated communities, verify token holdings, and control access to exclusive spaces"
    
    def __init__(self, 
                 rpc_url: str = "https://api.mainnet-beta.solana.com",
                 private_key_path: Optional[str] = None,
                 indexer_api_key: Optional[str] = None,
                 verification_api_url: Optional[str] = None,
                 **kwargs):
        super().__init__(rpc_url=rpc_url, private_key_path=private_key_path, 
                         indexer_api_key=indexer_api_key, **kwargs)
        
        # API endpoints for verification services
        self.verification_api_url = verification_api_url or "https://api.tokenverification.example/v1"
        
        # In-memory storage for community definitions and access rules
        self.communities = {}
        self.access_tokens = {}
        self.verification_cache = {}
        self.cache_expiration = 300  # 5 minutes
    
    @property
    def parameters(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "create_community", "configure_requirements", "verify_access", 
                        "generate_access_token", "verify_token", "list_communities",
                        "get_community_stats", "add_member", "remove_member",
                        "check_member_status", "get_members"
                    ],
                    "description": "The token-gated community action to perform"
                },
                "community_id": {
                    "type": "string",
                    "description": "ID of the community to interact with"
                },
                "community_name": {
                    "type": "string",
                    "description": "Name of the community (for creation)"
                },
                "description": {
                    "type": "string",
                    "description": "Description of the community"
                },
                "token_address": {
                    "type": "string",
                    "description": "Address of the token required for access"
                },
                "min_token_amount": {
                    "type": "number",
                    "description": "Minimum amount of tokens required for access"
                },
                "nft_collection_address": {
                    "type": "string",
                    "description": "Address of the NFT collection required for access"
                },
                "token_type": {
                    "type": "string",
                    "enum": ["fungible", "nft", "multi"],
                    "description": "Type of token required for access"
                },
                "wallet_address": {
                    "type": "string",
                    "description": "Wallet address to verify or grant access to"
                },
                "access_level": {
                    "type": "string",
                    "enum": ["member", "moderator", "admin"],
                    "description": "Access level to grant to the wallet"
                },
                "token_expiration": {
                    "type": "integer",
                    "description": "Expiration time for access token in seconds"
                },
                "blockchain": {
                    "type": "string",
                    "enum": ["solana", "ethereum", "polygon"],
                    "description": "Blockchain network for token verification"
                }
            },
            "required": ["action"]
        }
    
    def execute(self, **kwargs) -> Union[Dict[str, Any], ToolResult]:
        """Execute the token-gated community tool with the given parameters"""
        action = kwargs.get("action")
        
        try:
            if action == "create_community":
                return self._create_community(
                    community_name=kwargs.get("community_name", ""),
                    description=kwargs.get("description", ""),
                    token_address=kwargs.get("token_address"),
                    min_token_amount=kwargs.get("min_token_amount", 1),
                    token_type=kwargs.get("token_type", "fungible"),
                    nft_collection_address=kwargs.get("nft_collection_address")
                )
            elif action == "configure_requirements":
                return self._configure_requirements(
                    community_id=kwargs.get("community_id"),
                    token_address=kwargs.get("token_address"),
                    min_token_amount=kwargs.get("min_token_amount"),
                    token_type=kwargs.get("token_type"),
                    nft_collection_address=kwargs.get("nft_collection_address")
                )
            elif action == "verify_access":
                return self._verify_access(
                    community_id=kwargs.get("community_id"),
                    wallet_address=kwargs.get("wallet_address"),
                    blockchain=kwargs.get("blockchain", "solana")
                )
            elif action == "generate_access_token":
                return self._generate_access_token(
                    community_id=kwargs.get("community_id"),
                    wallet_address=kwargs.get("wallet_address"),
                    access_level=kwargs.get("access_level", "member"),
                    expiration=kwargs.get("token_expiration", 86400)  # Default: 24 hours
                )
            elif action == "verify_token":
                return self._verify_token(
                    access_token=kwargs.get("access_token")
                )
            elif action == "list_communities":
                return self._list_communities()
            elif action == "get_community_stats":
                return self._get_community_stats(
                    community_id=kwargs.get("community_id")
                )
            elif action == "add_member":
                return self._add_member(
                    community_id=kwargs.get("community_id"),
                    wallet_address=kwargs.get("wallet_address"),
                    access_level=kwargs.get("access_level", "member")
                )
            elif action == "remove_member":
                return self._remove_member(
                    community_id=kwargs.get("community_id"),
                    wallet_address=kwargs.get("wallet_address")
                )
            elif action == "check_member_status":
                return self._check_member_status(
                    community_id=kwargs.get("community_id"),
                    wallet_address=kwargs.get("wallet_address")
                )
            elif action == "get_members":
                return self._get_members(
                    community_id=kwargs.get("community_id"),
                    access_level=kwargs.get("access_level")
                )
            else:
                return ToolResult(
                    tool_name=self.name,
                    status="error",
                    error=f"Unknown token-gated community action: {action}"
                )
        except Exception as e:
            logging.error(f"Error executing token-gated community action {action}: {e}")
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Error executing token-gated community action {action}: {str(e)}"
            )
    
    def _create_community(self, community_name: str, description: str = "",
                        token_address: Optional[str] = None, min_token_amount: float = 1,
                        token_type: str = "fungible", nft_collection_address: Optional[str] = None) -> ToolResult:
        """Create a new token-gated community"""
        if not community_name:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Community name is required"
            )
        
        # For token-gated communities, we need token information
        if not token_address and not nft_collection_address:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Either token_address or nft_collection_address is required"
            )
        
        # Generate a unique community ID
        community_id = f"community_{int(time.time())}_{hashlib.md5(community_name.encode()).hexdigest()[:8]}"
        
        # Create community structure
        community = {
            "id": community_id,
            "name": community_name,
            "description": description,
            "created_at": self.format_timestamp(),
            "created_by": self._wallet_address or "anonymous",
            "requirements": {
                "token_type": token_type,
                "token_address": token_address,
                "min_token_amount": min_token_amount,
                "nft_collection_address": nft_collection_address
            },
            "members": {
                "admins": [self._wallet_address] if self._wallet_address else [],
                "moderators": [],
                "members": []
            },
            "stats": {
                "total_members": 0,
                "access_requests": 0,
                "access_granted": 0,
                "access_denied": 0
            }
        }
        
        # Store the community
        self.communities[community_id] = community
        
        return ToolResult.success(
            tool_name=self.name,
            result={
                "community_id": community_id,
                "name": community_name,
                "requirements": community["requirements"],
                "created_at": community["created_at"],
                "message": "Community created successfully"
            }
        )
    
    def _configure_requirements(self, community_id: str, token_address: Optional[str] = None,
                              min_token_amount: Optional[float] = None, token_type: Optional[str] = None,
                              nft_collection_address: Optional[str] = None) -> ToolResult:
        """Configure access requirements for a community"""
        if not community_id or community_id not in self.communities:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Community with ID {community_id} not found"
            )
        
        # Get the community
        community = self.communities[community_id]
        
        # Check if caller is an admin
        if self._wallet_address and self._wallet_address not in community["members"]["admins"]:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Only community admins can configure requirements"
            )
        
        # Update requirements
        requirements = community["requirements"]
        
        if token_type:
            requirements["token_type"] = token_type
        
        if token_address:
            requirements["token_address"] = token_address
        
        if min_token_amount is not None:
            requirements["min_token_amount"] = min_token_amount
        
        if nft_collection_address:
            requirements["nft_collection_address"] = nft_collection_address
        
        # Update the community
        community["requirements"] = requirements
        self.communities[community_id] = community
        
        return ToolResult.success(
            tool_name=self.name,
            result={
                "community_id": community_id,
                "requirements": requirements,
                "updated_at": self.format_timestamp(),
                "message": "Community requirements updated successfully"
            }
        )
    
    def _verify_access(self, community_id: str, wallet_address: str,
                      blockchain: str = "solana") -> ToolResult:
        """Verify if a wallet has access to a community based on token holdings"""
        if not community_id or community_id not in self.communities:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Community with ID {community_id} not found"
            )
        
        if not wallet_address:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Wallet address is required"
            )
        
        # Get the community
        community = self.communities[community_id]
        requirements = community["requirements"]
        
        # Check if wallet is already a member
        if (wallet_address in community["members"]["admins"] or
            wallet_address in community["members"]["moderators"] or
            wallet_address in community["members"]["members"]):
            
            return ToolResult.success(
                tool_name=self.name,
                result={
                    "community_id": community_id,
                    "wallet_address": wallet_address,
                    "has_access": True,
                    "reason": "Already a member",
                    "verification_time": self.format_timestamp()
                }
            )
        
        # Check cache first
        cache_key = f"{wallet_address}_{community_id}_{blockchain}"
        if cache_key in self.verification_cache:
            cache_entry = self.verification_cache[cache_key]
            # Only use cache if not expired
            if time.time() - cache_entry["timestamp"] < self.cache_expiration:
                return ToolResult.success(
                    tool_name=self.name,
                    result=cache_entry["data"]
                )
        
        # Verify token holdings
        token_type = requirements.get("token_type", "fungible")
        
        if token_type == "fungible":
            token_address = requirements.get("token_address")
            min_amount = requirements.get("min_token_amount", 1)
            
            # In a real implementation, we would query the blockchain
            # Here, we'll simulate a token balance check
            holdings = self._simulate_token_holdings(wallet_address, token_address, blockchain)
            has_access = holdings >= min_amount
            
            result = {
                "community_id": community_id,
                "wallet_address": wallet_address,
                "has_access": has_access,
                "token_address": token_address,
                "required_amount": min_amount,
                "actual_amount": holdings,
                "blockchain": blockchain,
                "verification_time": self.format_timestamp()
            }
            
        elif token_type == "nft":
            collection_address = requirements.get("nft_collection_address")
            
            # In a real implementation, we would query the blockchain
            # Here, we'll simulate an NFT ownership check
            owned_nfts = self._simulate_nft_holdings(wallet_address, collection_address, blockchain)
            has_access = len(owned_nfts) > 0
            
            result = {
                "community_id": community_id,
                "wallet_address": wallet_address,
                "has_access": has_access,
                "nft_collection": collection_address,
                "owned_nfts": owned_nfts,
                "required_nfts": 1,
                "blockchain": blockchain,
                "verification_time": self.format_timestamp()
            }
        
        else:  # multi
            # More complex verification for multiple token types
            has_access = self._simulate_multi_token_verification(wallet_address, requirements, blockchain)
            
            result = {
                "community_id": community_id,
                "wallet_address": wallet_address,
                "has_access": has_access,
                "requirements": requirements,
                "blockchain": blockchain,
                "verification_time": self.format_timestamp()
            }
        
        # Update stats
        community["stats"]["access_requests"] += 1
        if has_access:
            community["stats"]["access_granted"] += 1
        else:
            community["stats"]["access_denied"] += 1
        
        # Cache the result
        self.verification_cache[cache_key] = {
            "timestamp": time.time(),
            "data": result
        }
        
        return ToolResult.success(
            tool_name=self.name,
            result=result
        )
    
    def _generate_access_token(self, community_id: str, wallet_address: str,
                             access_level: str = "member", expiration: int = 86400) -> ToolResult:
        """Generate a temporary access token for a wallet"""
        if not community_id or community_id not in self.communities:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Community with ID {community_id} not found"
            )
        
        if not wallet_address:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Wallet address is required"
            )
        
        # Verify access first
        verify_result = self._verify_access(community_id, wallet_address)
        if verify_result.status != "success" or not verify_result.result.get("has_access", False):
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Wallet does not have access to this community"
            )
        
        # Generate token (in a real implementation, this would be a JWT)
        token_id = hashlib.sha256(f"{wallet_address}_{community_id}_{time.time()}".encode()).hexdigest()
        
        # Token data
        token_data = {
            "token_id": token_id,
            "community_id": community_id,
            "wallet_address": wallet_address,
            "access_level": access_level,
            "issued_at": time.time(),
            "expires_at": time.time() + expiration
        }
        
        # Store token
        self.access_tokens[token_id] = token_data
        
        # Create encoded token (simulated JWT)
        encoded_token = base64.b64encode(json.dumps(token_data).encode()).decode()
        
        return ToolResult.success(
            tool_name=self.name,
            result={
                "access_token": encoded_token,
                "token_id": token_id,
                "community_id": community_id,
                "wallet_address": wallet_address,
                "access_level": access_level,
                "issued_at": self.format_timestamp(token_data["issued_at"]),
                "expires_at": self.format_timestamp(token_data["expires_at"]),
                "message": "Access token generated successfully"
            }
        )
    
    def _verify_token(self, access_token: str) -> ToolResult:
        """Verify an access token's validity"""
        if not access_token:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Access token is required"
            )
        
        try:
            # Decode token
            token_data_json = base64.b64decode(access_token).decode()
            token_data = json.loads(token_data_json)
            
            token_id = token_data.get("token_id")
            
            # Check if token exists
            if token_id not in self.access_tokens:
                return ToolResult(
                    tool_name=self.name,
                    status="error",
                    error="Invalid access token"
                )
            
            # Check if token is expired
            if time.time() > token_data.get("expires_at", 0):
                return ToolResult(
                    tool_name=self.name,
                    status="error",
                    error="Access token has expired"
                )
            
            # Check if community still exists
            community_id = token_data.get("community_id")
            if community_id not in self.communities:
                return ToolResult(
                    tool_name=self.name,
                    status="error",
                    error="Community no longer exists"
                )
            
            # Token is valid
            return ToolResult.success(
                tool_name=self.name,
                result={
                    "token_id": token_id,
                    "is_valid": True,
                    "community_id": community_id,
                    "wallet_address": token_data.get("wallet_address"),
                    "access_level": token_data.get("access_level"),
                    "expires_at": self.format_timestamp(token_data.get("expires_at")),
                    "time_remaining_seconds": int(token_data.get("expires_at", 0) - time.time())
                }
            )
            
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Error verifying token: {str(e)}"
            )
    
    def _list_communities(self) -> ToolResult:
        """List all available communities"""
        communities_list = []
        
        for community_id, community in self.communities.items():
            communities_list.append({
                "id": community_id,
                "name": community.get("name", ""),
                "description": community.get("description", ""),
                "requirements": community.get("requirements", {}),
                "total_members": community.get("stats", {}).get("total_members", 0),
                "created_at": community.get("created_at", "")
            })
        
        return ToolResult.success(
            tool_name=self.name,
            result={
                "communities": communities_list,
                "count": len(communities_list),
                "timestamp": self.format_timestamp()
            }
        )
    
    def _get_community_stats(self, community_id: str) -> ToolResult:
        """Get statistics for a community"""
        if not community_id or community_id not in self.communities:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Community with ID {community_id} not found"
            )
        
        community = self.communities[community_id]
        
        # Calculate additional statistics
        members = community.get("members", {})
        admin_count = len(members.get("admins", []))
        moderator_count = len(members.get("moderators", []))
        member_count = len(members.get("members", []))
        total_members = admin_count + moderator_count + member_count
        
        # Update total members count
        community["stats"]["total_members"] = total_members
        
        return ToolResult.success(
            tool_name=self.name,
            result={
                "community_id": community_id,
                "name": community.get("name", ""),
                "stats": {
                    "total_members": total_members,
                    "admin_count": admin_count,
                    "moderator_count": moderator_count,
                    "member_count": member_count,
                    "access_requests": community.get("stats", {}).get("access_requests", 0),
                    "access_granted": community.get("stats", {}).get("access_granted", 0),
                    "access_denied": community.get("stats", {}).get("access_denied", 0)
                },
                "requirements": community.get("requirements", {}),
                "created_at": community.get("created_at", ""),
                "timestamp": self.format_timestamp()
            }
        )
    
    def _add_member(self, community_id: str, wallet_address: str,
                  access_level: str = "member") -> ToolResult:
        """Add a member to a community with specified access level"""
        if not community_id or community_id not in self.communities:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Community with ID {community_id} not found"
            )
        
        if not wallet_address:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Wallet address is required"
            )
        
        # Check if access level is valid
        if access_level not in ["member", "moderator", "admin"]:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Invalid access level: {access_level}"
            )
        
        community = self.communities[community_id]
        
        # Check if caller is authorized (only admins can add moderators/admins)
        if access_level in ["moderator", "admin"]:
            if not self._wallet_address or self._wallet_address not in community["members"]["admins"]:
                return ToolResult(
                    tool_name=self.name,
                    status="error",
                    error="Only community admins can add moderators or admins"
                )
        
        # Check if member already exists in any role
        for role, members in community["members"].items():
            if wallet_address in members:
                # If already in the correct role, nothing to do
                if role == f"{access_level}s":  # Note the plural
                    return ToolResult.success(
                        tool_name=self.name,
                        result={
                            "community_id": community_id,
                            "wallet_address": wallet_address,
                            "access_level": access_level,
                            "message": f"Wallet is already a {access_level} of this community"
                        }
                    )
                # Otherwise, remove from current role
                community["members"][role].remove(wallet_address)
        
        # Add to the appropriate role
        role_key = f"{access_level}s"  # Convert to plural
        community["members"][role_key].append(wallet_address)
        
        # Update stats
        community["stats"]["total_members"] =