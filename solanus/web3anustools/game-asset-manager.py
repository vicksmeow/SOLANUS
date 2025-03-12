from typing import Dict, Any, Optional, List, Union
import logging
from anus.tools.web3.gamefi_base_tool import GameFiBaseTool
from anus.tools.base.tool_result import ToolResult

class GameAssetManager(GameFiBaseTool):
    """
    Tool for managing in-game assets across different blockchain games.
    Supports inventory management, asset transfers, and marketplace interactions.
    """
    name = "game_asset_manager"
    description = "Manage in-game assets, inventory, and marketplace transactions for blockchain games"
    
    @property
    def parameters(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "list_assets", "get_asset_details", "transfer_asset", 
                        "list_games", "get_inventory", "check_asset_value",
                        "list_marketplace", "buy_asset", "sell_asset"
                    ],
                    "description": "The game asset action to perform"
                },
                "game_id": {
                    "type": "string",
                    "description": "Identifier for the game"
                },
                "asset_id": {
                    "type": "string",
                    "description": "Identifier for the asset"
                },
                "wallet_address": {
                    "type": "string",
                    "description": "Wallet address for inventory lookup or transfers"
                },
                "recipient_address": {
                    "type": "string",
                    "description": "Recipient wallet address for transfers"
                },
                "quantity": {
                    "type": "integer",
                    "description": "Quantity of assets for transactions"
                },
                "price": {
                    "type": "number",
                    "description": "Price for buying or selling assets"
                },
                "marketplace": {
                    "type": "string",
                    "description": "Marketplace for buying/selling (e.g., in-game, opensea)"
                },
                "asset_type": {
                    "type": "string",
                    "description": "Type of asset (e.g., character, weapon, land)"
                }
            },
            "required": ["action"]
        }
    
    def execute(self, **kwargs) -> Union[Dict[str, Any], ToolResult]:
        """Execute the game asset manager tool with given parameters"""
        action = kwargs.get("action")
        
        try:
            if action == "list_assets":
                return self._list_assets(
                    game_id=kwargs.get("game_id"),
                    asset_type=kwargs.get("asset_type")
                )
            elif action == "get_asset_details":
                return self._get_asset_details(
                    game_id=kwargs.get("game_id"),
                    asset_id=kwargs.get("asset_id")
                )
            elif action == "transfer_asset":
                return self._transfer_asset(
                    game_id=kwargs.get("game_id"),
                    asset_id=kwargs.get("asset_id"),
                    recipient_address=kwargs.get("recipient_address"),
                    quantity=kwargs.get("quantity", 1)
                )
            elif action == "list_games":
                return self._list_games()
            elif action == "get_inventory":
                return self._get_inventory(
                    game_id=kwargs.get("game_id"),
                    wallet_address=kwargs.get("wallet_address")
                )
            elif action == "check_asset_value":
                return self._check_asset_value(
                    game_id=kwargs.get("game_id"),
                    asset_id=kwargs.get("asset_id")
                )
            elif action == "list_marketplace":
                return self._list_marketplace(
                    game_id=kwargs.get("game_id"),
                    asset_type=kwargs.get("asset_type")
                )
            elif action == "buy_asset":
                return self._buy_asset(
                    game_id=kwargs.get("game_id"),
                    asset_id=kwargs.get("asset_id"),
                    price=kwargs.get("price"),
                    quantity=kwargs.get("quantity", 1),
                    marketplace=kwargs.get("marketplace", "in-game")
                )
            elif action == "sell_asset":
                return self._sell_asset(
                    game_id=kwargs.get("game_id"),
                    asset_id=kwargs.get("asset_id"),
                    price=kwargs.get("price"),
                    quantity=kwargs.get("quantity", 1),
                    marketplace=kwargs.get("marketplace", "in-game")
                )
            else:
                return ToolResult(
                    tool_name=self.name,
                    status="error",
                    error=f"Unknown game asset action: {action}"
                )
        except Exception as e:
            logging.error(f"Error executing game asset action {action}: {e}")
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Error executing game asset action {action}: {str(e)}"
            )
    
    def _list_assets(self, game_id: Optional[str] = None, 
                   asset_type: Optional[str] = None) -> ToolResult:
        """List available assets for a game"""
        if not game_id:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Game ID is required"
            )
        
        # Simulated asset data - in a real implementation, this would query a game API
        assets = self._simulate_game_assets(game_id, asset_type)
        
        return ToolResult.success(
            tool_name=self.name,
            result={
                "game_id": game_id,
                "asset_type": asset_type,
                "assets": assets,
                "count": len(assets)
            }
        )
    
    def _get_asset_details(self, game_id: str, asset_id: str) -> ToolResult:
        """Get detailed information about a specific game asset"""
        if not game_id or not asset_id:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Game ID and asset ID are required"
            )
        
        # Simulated asset details
        asset_details = self._simulate_asset_details(game_id, asset_id)
        
        if not asset_details:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Asset with ID {asset_id} not found in game {game_id}"
            )
        
        return ToolResult.success(
            tool_name=self.name,
            result=asset_details
        )
    
    def _transfer_asset(self, game_id: str, asset_id: str, 
                      recipient_address: str, quantity: int = 1) -> ToolResult:
        """Transfer an asset to another wallet"""
        if not self._wallet_address:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Wallet not loaded. Please load a wallet first."
            )
        
        if not game_id or not asset_id or not recipient_address:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Game ID, asset ID, and recipient address are required"
            )
        
        # Check if user owns the asset and has enough quantity
        inventory = self._simulate_inventory(game_id, self._wallet_address)
        owned_assets = [asset for asset in inventory if asset["asset_id"] == asset_id]
        
        if not owned_assets:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"You don't own any asset with ID {asset_id}"
            )
        
        owned_asset = owned_assets[0]
        if owned_asset["quantity"] < quantity:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Insufficient quantity. You own {owned_asset['quantity']} but tried to transfer {quantity}."
            )
        
        # In a real implementation, this would execute the transfer on-chain
        # For simulation, we'll just return success
        return ToolResult.success(
            tool_name=self.name,
            result={
                "transaction_id": f"tx_{int(time.time())}_{asset_id[:6]}",
                "sender": self._wallet_address,
                "recipient": recipient_address,
                "game_id": game_id,
                "asset_id": asset_id,
                "asset_name": owned_asset["name"],
                "quantity": quantity,
                "status": "completed",
                "timestamp": int(time.time())
            }
        )
    
    def _list_games(self) -> ToolResult:
        """List supported blockchain games"""
        # Simulated list of supported games
        games = [
            {
                "id": "axie-infinity",
                "name": "Axie Infinity",
                "blockchain": "ronin",
                "website": "https://axieinfinity.com/",
                "description": "Collect, battle, and earn with fantasy creatures called Axies"
            },
            {
                "id": "gods-unchained",
                "name": "Gods Unchained",
                "blockchain": "ethereum",
                "website": "https://godsunchained.com/",
                "description": "Free-to-play tactical card game that gives players true ownership of their in-game items"
            },
            {
                "id": "star-atlas",
                "name": "Star Atlas",
                "blockchain": "solana",
                "website": "https://staratlas.com/",
                "description": "Next-gen metaverse with AAA-quality game experience built on Solana"
            },
            {
                "id": "illuvium",
                "name": "Illuvium",
                "blockchain": "ethereum",
                "website": "https://illuvium.io/",
                "description": "Auto-battler RPG with a vast open world to explore"
            },
            {
                "id": "the-sandbox",
                "name": "The Sandbox",
                "blockchain": "ethereum",
                "website": "https://www.sandbox.game/",
                "description": "Virtual world where players can build, own, and monetize their gaming experiences"
            }
        ]
        
        return ToolResult.success(
            tool_name=self.name,
            result={
                "games": games,
                "count": len(games)
            }
        )
    
    def _get_inventory(self, game_id: str, wallet_address: Optional[str] = None) -> ToolResult:
        """Get inventory of in-game assets for a wallet"""
        if not game_id:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Game ID is required"
            )
        
        # Use provided wallet address or default to loaded wallet
        wallet = wallet_address or self._wallet_address
        if not wallet:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Wallet address is required"
            )
        
        # Simulated inventory data
        inventory = self._simulate_inventory(game_id, wallet)
        
        # Calculate total value of inventory
        total_value = sum(asset.get("value", 0) * asset.get("quantity", 1) for asset in inventory)
        
        return ToolResult.success(
            tool_name=self.name,
            result={
                "game_id": game_id,
                "wallet_address": wallet,
                "inventory": inventory,
                "asset_count": len(inventory),
                "total_items": sum(asset.get("quantity", 1) for asset in inventory),
                "total_value": total_value,
                "currency": self._get_game_currency(game_id)
            }
        )
    
    def _check_asset_value(self, game_id: str, asset_id: str) -> ToolResult:
        """Check the current market value of an asset"""
        if not game_id or not asset_id:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Game ID and asset ID are required"
            )
        
        # Simulated asset value data
        value_data = self._simulate_asset_value(game_id, asset_id)
        
        if not value_data:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Asset with ID {asset_id} not found in game {game_id}"
            )
        
        return ToolResult.success(
            tool_name=self.name,
            result=value_data
        )
    
    def _list_marketplace(self, game_id: str, asset_type: Optional[str] = None) -> ToolResult:
        """List assets available on the marketplace"""
        if not game_id:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Game ID is required"
            )
        
        # Simulated marketplace listings
        listings = self._simulate_marketplace_listings(game_id, asset_type)
        
        return ToolResult.success(
            tool_name=self.name,
            result={
                "game_id": game_id,
                "asset_type": asset_type,
                "listings": listings,
                "count": len(listings),
                "currency": self._get_game_currency(game_id)
            }
        )
    
    def _buy_asset(self, game_id: str, asset_id: str, price: float,
                 quantity: int = 1, marketplace: str = "in-game") -> ToolResult:
        """Buy an asset from the marketplace"""
        if not self._wallet_address:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Wallet not loaded. Please load a wallet first."
            )
        
        if not game_id or not asset_id:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Game ID and asset ID are required"
            )
        
        if price is None:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Price is required"
            )
        
        # Check if asset is available on marketplace
        listings = self._simulate_marketplace_listings(game_id, None)
        matching_listings = [listing for listing in listings if listing["asset_id"] == asset_id]
        
        if not matching_listings:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Asset with ID {asset_id} not found on the marketplace"
            )
        
        listing = matching_listings[0]
        if listing["price"] != price:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Price mismatch. Listed price is {listing['price']} but you offered {price}."
            )
        
        if listing["quantity_available"] < quantity:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Insufficient quantity available. Only {listing['quantity_available']} available but you tried to buy {quantity}."
            )
        
        # In a real implementation, this would execute the purchase on-chain
        # For simulation, we'll just return success
        return ToolResult.success(
            tool_name=self.name,
            result={
                "transaction_id": f"tx_{int(time.time())}_{asset_id[:6]}",
                "buyer": self._wallet_address,
                "seller": listing["seller"],
                "game_id": game_id,
                "asset_id": asset_id,
                "asset_name": listing["name"],
                "quantity": quantity,
                "price_per_unit": price,
                "total_price": price * quantity,
                "currency": self._get_game_currency(game_id),
                "marketplace": marketplace,
                "status": "completed",
                "timestamp": int(time.time())
            }
        )
    
    def _sell_asset(self, game_id: str, asset_id: str, price: float,
                  quantity: int = 1, marketplace: str = "in-game") -> ToolResult:
        """List an asset for sale on the marketplace"""
        if not self._wallet_address:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Wallet not loaded. Please load a wallet first."
            )
        
        if not game_id or not asset_id:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Game ID and asset ID are required"
            )
        
        if price is None:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Price is required"
            )
        
        # Check if user owns the asset and has enough quantity
        inventory = self._simulate_inventory(game_id, self._wallet_address)
        owned_assets = [asset for asset in inventory if asset["asset_id"] == asset_id]
        
        if not owned_assets:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"You don't own any asset with ID {asset_id}"
            )
        
        owned_asset = owned_assets[0]
        if owned_asset["quantity"] < quantity:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Insufficient quantity. You own {owned_asset['quantity']} but tried to sell {quantity}."
            )
        
        # In a real implementation, this would list the asset on-chain or in a marketplace
        # For simulation, we'll just return success
        return ToolResult.success(
            tool_name=self.name,
            result={
                "listing_id": f"list_{int(time.time())}_{asset_id[:6]}",
                "seller": self._wallet_address,
                "game_id": game_id,
                "asset_id": asset_id,
                "asset_name": owned_asset["name"],
                "quantity": quantity,
                "price_per_unit": price,
                "total_price": price * quantity,
                "currency": self._get_game_currency(game_id),
                "marketplace": marketplace,
                "status": "listed",
                "expiration": int(time.time()) + 7 * 24 * 60 * 60  # 7 days
            }
        )
    
    def _simulate_game_assets(self, game_id: str, asset_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Simulate a list of assets for a game"""
        # Asset templates by game
        asset_templates = {
            "axie-infinity": [
                {"type": "character", "rarity": "rare", "class": "aquatic"},
                {"type": "character", "rarity": "epic", "class": "beast"},
                {"type": "character", "rarity": "common", "class": "plant"},
                {"type": "land", "rarity": "common", "region": "savannah"},
                {"type": "item", "rarity": "epic", "category": "potion"}
            ],
            "gods-unchained": [
                {"type": "card", "rarity": "rare", "god": "nature"},
                {"type": "card", "rarity": "epic", "god": "death"},
                {"type": "card", "rarity": "legendary", "god": "light"},
                {"type": "card", "rarity": "common", "god": "war"},
                {"type": "cosmetic", "rarity": "epic", "category": "board"}
            ],
            "star-atlas": [
                {"type": "ship", "rarity": "rare", "faction": "oni"},
                {"type": "ship", "rarity": "epic", "faction": "mud"},
                {"type": "land", "rarity": "legendary", "region": "nebula"},
                {"type": "equipment", "rarity": "common", "category": "weapon"},
                {"type": "crew", "rarity": "rare", "role": "engineer"}
            ]
        }
        
        # Generic assets if game not found
        if game_id not in asset_templates:
            asset_templates[game_id] = [
                {"type": "character", "rarity": "common", "class": "warrior"},
                {"type": "weapon", "rarity": "rare", "category": "sword"},
                {"type": "armor", "rarity": "epic", "category": "helmet"},
                {"type": "consumable", "rarity": "common", "category": "potion"},
                {"type": "resource", "rarity": "common", "category": "wood"}
            ]
        
        templates = asset_templates[game_id]
        
        # Filter by asset type if specified
        if asset_type:
            templates = [t for t in templates if t["type"] == asset_type]
        
        # Generate assets from templates
        assets = []
        for i, template in enumerate(templates):
            asset_type = template["type"]
            rarity = template["rarity"]
            
            # Base properties
            asset = {
                "asset_id": f"{game_id}-{asset_type}-{i+1}",
                "name": f"{rarity.capitalize()} {asset_type.capitalize()} #{i+1}",
                "type": asset_type,
                "rarity": rarity,
                "game_id": game_id,
                "transferable": True,
                "metadata_uri": f"https://example.com/games/{game_id}/assets/{asset_type}-{i+1}"
            }
            
            # Add template-specific properties
            for key, value in template.items():
                if key not in ["type", "rarity"]:
                    asset[key] = value
            
            # Add generic stats
            stats = {}
            if asset_type in ["character", "ship", "card"]:
                stats["attack"] = 5 + (i * 2)
                stats["defense"] = 3 + i
                stats["health"] = 10 + (i * 3)
            elif asset_type in ["weapon", "equipment"]:
                stats["damage"] = 3 + (i * 2)
                stats["durability"] = 20 + (i * 5)
            elif asset_type == "land":
                stats["size"] = 10 + (i * 5)
                stats["resources"] = 2 + i
            
            if stats:
                asset["stats"] = stats
            
            assets.append(asset)
        
        return assets
    
    def _simulate_asset_details(self, game_id: str, asset_id: str) -> Optional[Dict[str, Any]]:
        """Simulate detailed information for a specific asset"""
        # Get all assets for the game
        all_assets = self._simulate_game_assets(game_id, None)
        
        # Find the specific asset
        matching_assets = [asset for asset in all_assets if asset["asset_id"] == asset_id]
        if not matching_assets:
            return None
        
        asset = matching_assets[0]
        
        # Add more detailed information
        asset_details = asset.copy()
        
        # Add description
        asset_details["description"] = f"A {asset['rarity']} {asset['type']} from the game {game_id.replace('-', ' ').title()}."
        
        # Add value
        rarity_multiplier = {
            "common": 1,
            "uncommon": 2,
            "rare": 5,
            "epic": 10,
            "legendary": 25,
            "mythic": 100
        }
        base_value = 10
        multiplier = rarity_multiplier.get(asset["rarity"], 1)
        asset_details["value"] = base_value * multiplier
        
        # Add attributes/traits
        attributes = []
        for key, value in asset.items():
            if key not in ["asset_id", "name", "type", "rarity", "game_id", "transferable", "metadata_uri", "stats"]:
                attributes.append({
                    "trait_type": key,
                    "value": value
                })
        
        # Add some random attributes
        if asset["type"] == "character":
            attributes.append({"trait_type": "level", "value": 1 + (hash(asset_id) % 100)})
            attributes.append({"trait_type": "experience", "value": 0 + (hash(asset_id) % 1000)})
        
        asset_details["attributes"] = attributes
        
        # Add history
        asset_details["creation_date"] = "2023-01-01T00:00:00Z"
        asset_details["last_transfer_date"] = "2023-06-15T12:34:56Z"
        
        return asset_details
    
    def _simulate_inventory(self, game_id: str, wallet_address: str) -> List[Dict[str, Any]]:
        """Simulate inventory for a wallet"""
        # Get all assets for the game
        all_assets = self._simulate_game_assets(game_id, None)
        
        # Deterministically select some assets based on wallet address
        wallet_hash = hash(wallet_address)
        asset_count = (wallet_hash % 8) + 2  # 2-9 assets
        
        inventory = []
        for i in range(min(asset_count, len(all_assets))):
            asset_index = (wallet_hash + i) % len(all_assets)
            asset = all_assets[asset_index].copy()
            
            # Add quantity and acquisition information
            asset["quantity"] = ((wallet_hash + i) % 5) + 1
            asset["acquisition_date"] = "2023-06-15T12:34:56Z"
            
            # Add value
            rarity_multiplier = {
                "common": 1,
                "uncommon": 2,
                "rare": 5,
                "epic": 10,
                "legendary": 25,
                "mythic": 100
            }
            base_value = 10
            multiplier = rarity_multiplier.get(asset["rarity"], 1)
            asset["value"] = base_value * multiplier
            
            inventory.append(asset)
        
        return inventory
    
    def _simulate_asset_value(self, game_id: str,