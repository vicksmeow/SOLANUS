from typing import Dict, Any, Optional, List, Union
import json
import time
import base64
import logging
from anus.tools.base.tool import BaseTool
from anus.tools.base.tool_result import ToolResult

class SolanaTool(BaseTool):
    """
    Tool for interacting with the Solana blockchain.
    Provides capabilities for wallet management, transactions, and contract interaction.
    """
    name = "solana"
    description = "Interact with the Solana blockchain, manage wallets, and execute transactions"
    
    def __init__(self, 
                 rpc_url: str = "https://api.mainnet-beta.solana.com", 
                 private_key_path: Optional[str] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.rpc_url = rpc_url
        self.private_key_path = private_key_path
        self._client = None
        self._keypair = None
        self._wallet_address = None
        
        # Initialize solana client
        self._initialize_client()
        
        # Load wallet if private key is provided
        if private_key_path:
            self._load_wallet()
    
    @property
    def parameters(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_balance", "create_wallet", "transfer_sol", "get_token_balance", 
                        "transfer_token", "get_transaction", "get_account_info",
                        "create_token", "mint_token", "get_token_supply", "swap_tokens",
                        "provide_liquidity", "stake_sol", "unstake_sol", "create_nft",
                        "get_price", "get_gas_estimate", "get_network_status"
                    ],
                    "description": "The Solana blockchain action to perform"
                },
                "wallet_address": {
                    "type": "string",
                    "description": "Solana wallet address (Public key)"
                },
                "recipient_address": {
                    "type": "string",
                    "description": "Recipient wallet address for transfers"
                },
                "amount": {
                    "type": "number",
                    "description": "Amount of SOL or tokens to transfer"
                },
                "token_address": {
                    "type": "string", 
                    "description": "SPL token mint address"
                },
                "transaction_signature": {
                    "type": "string",
                    "description": "Transaction signature to look up"
                },
                "token_name": {
                    "type": "string",
                    "description": "Name for a new token"
                },
                "token_symbol": {
                    "type": "string",
                    "description": "Symbol for a new token"
                },
                "token_decimals": {
                    "type": "integer",
                    "description": "Decimals for a new token"
                },
                "token_supply": {
                    "type": "number",
                    "description": "Initial supply for a new token"
                },
                "from_token": {
                    "type": "string",
                    "description": "Token address to swap from"
                },
                "to_token": {
                    "type": "string",
                    "description": "Token address to swap to"
                },
                "slippage": {
                    "type": "number",
                    "description": "Slippage tolerance for swaps (percentage)"
                },
                "nft_metadata": {
                    "type": "object",
                    "description": "Metadata for NFT creation"
                }
            },
            "required": ["action"]
        }
    
    def _initialize_client(self):
        """Initialize Solana client"""
        try:
            # We're using dynamic imports to handle optional dependencies
            from solana.rpc.api import Client
            self._client = Client(self.rpc_url)
            logging.info(f"Solana client initialized with RPC URL: {self.rpc_url}")
        except ImportError:
            logging.error("Solana package not installed. Please install with 'pip install solana'")
            raise ImportError("Solana package required for SolanaTool. Install with 'pip install solana'")
    
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
    
    def execute(self, **kwargs) -> Union[Dict[str, Any], ToolResult]:
        """Execute the Solana tool with the given parameters"""
        action = kwargs.get("action")
        
        try:
            if action == "get_balance":
                return self._get_balance(kwargs.get("wallet_address", self._wallet_address))
            elif action == "create_wallet":
                return self._create_wallet()
            elif action == "transfer_sol":
                return self._transfer_sol(
                    recipient_address=kwargs.get("recipient_address"),
                    amount=kwargs.get("amount")
                )
            elif action == "get_token_balance":
                return self._get_token_balance(
                    wallet_address=kwargs.get("wallet_address", self._wallet_address),
                    token_address=kwargs.get("token_address")
                )
            elif action == "transfer_token":
                return self._transfer_token(
                    recipient_address=kwargs.get("recipient_address"),
                    token_address=kwargs.get("token_address"),
                    amount=kwargs.get("amount")
                )
            elif action == "get_transaction":
                return self._get_transaction(kwargs.get("transaction_signature"))
            elif action == "get_account_info":
                return self._get_account_info(kwargs.get("wallet_address", self._wallet_address))
            elif action == "create_token":
                return self._create_token(
                    token_name=kwargs.get("token_name"),
                    token_symbol=kwargs.get("token_symbol"),
                    token_decimals=kwargs.get("token_decimals", 9),
                    token_supply=kwargs.get("token_supply", 0)
                )
            elif action == "mint_token":
                return self._mint_token(
                    token_address=kwargs.get("token_address"),
                    recipient_address=kwargs.get("recipient_address", self._wallet_address),
                    amount=kwargs.get("amount")
                )
            elif action == "get_token_supply":
                return self._get_token_supply(kwargs.get("token_address"))
            elif action == "swap_tokens":
                return self._swap_tokens(
                    from_token=kwargs.get("from_token"),
                    to_token=kwargs.get("to_token"),
                    amount=kwargs.get("amount"),
                    slippage=kwargs.get("slippage", 0.5)
                )
            elif action == "provide_liquidity":
                return self._provide_liquidity(
                    token_a=kwargs.get("token_a"),
                    token_b=kwargs.get("token_b"),
                    amount_a=kwargs.get("amount_a"),
                    amount_b=kwargs.get("amount_b")
                )
            elif action == "stake_sol":
                return self._stake_sol(
                    amount=kwargs.get("amount"),
                    validator=kwargs.get("validator")
                )
            elif action == "create_nft":
                return self._create_nft(
                    nft_metadata=kwargs.get("nft_metadata", {})
                )
            elif action == "get_price":
                return self._get_price(
                    token_address=kwargs.get("token_address", "So11111111111111111111111111111111111111112")  # SOL by default
                )
            elif action == "get_network_status":
                return self._get_network_status()
            else:
                return ToolResult(
                    tool_name=self.name,
                    status="error",
                    error=f"Unknown Solana action: {action}"
                )
        except Exception as e:
            logging.error(f"Error executing Solana action {action}: {e}")
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Error executing Solana action {action}: {str(e)}"
            )
    
    def _get_balance(self, wallet_address: Optional[str] = None) -> ToolResult:
        """Get SOL balance for a wallet address"""
        if not wallet_address:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Wallet address is required"
            )
        
        try:
            response = self._client.get_balance(wallet_address)
            if response["result"]["value"] is not None:
                # Convert lamports to SOL (1 SOL = 10^9 lamports)
                balance_lamports = response["result"]["value"]
                balance_sol = balance_lamports / 10**9
                
                return ToolResult.success(
                    tool_name=self.name,
                    result={
                        "wallet_address": wallet_address,
                        "balance_lamports": balance_lamports,
                        "balance_sol": balance_sol,
                        "unit": "SOL"
                    }
                )
            else:
                return ToolResult(
                    tool_name=self.name,
                    status="error",
                    error=f"Failed to get balance for {wallet_address}"
                )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Error getting balance: {str(e)}"
            )
    
    def _create_wallet(self) -> ToolResult:
        """Create a new Solana wallet"""
        try:
            from solana.keypair import Keypair
            
            # Generate a new keypair
            new_keypair = Keypair()
            wallet_address = str(new_keypair.public_key)
            
            # Convert private key to JSON-serializable format
            private_key_bytes = list(new_keypair.secret_key)
            
            # Generate a timestamp-based filename for the private key
            timestamp = int(time.time())
            key_filename = f"solana_keypair_{timestamp}.json"
            
            # Save private key to file (in practice, this should be encrypted)
            with open(key_filename, 'w') as f:
                json.dump(private_key_bytes, f)
            
            return ToolResult.success(
                tool_name=self.name,
                result={
                    "wallet_address": wallet_address,
                    "private_key_file": key_filename,
                    "message": "IMPORTANT: Keep your private key secure and never share it"
                }
            )
        except ImportError:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Solana package not installed. Please install with 'pip install solana'"
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Error creating wallet: {str(e)}"
            )
    
    def _transfer_sol(self, recipient_address: str, amount: float) -> ToolResult:
        """Transfer SOL to another wallet"""
        if not self._keypair:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Private key not loaded. Please load a wallet first."
            )
        
        if not recipient_address:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Recipient address is required"
            )
        
        if not amount or amount <= 0:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Valid amount is required (must be greater than 0)"
            )
        
        try:
            from solana.transaction import Transaction
            from solana.system_program import TransferParams, transfer
            from solana.publickey import PublicKey
            
            # Convert amount to lamports
            lamports = int(amount * 10**9)
            
            # Create transfer instruction
            transfer_instruction = transfer(
                TransferParams(
                    from_pubkey=self._keypair.public_key,
                    to_pubkey=PublicKey(recipient_address),
                    lamports=lamports
                )
            )
            
            # Create and sign transaction
            transaction = Transaction().add(transfer_instruction)
            transaction_signature = self._client.send_transaction(
                transaction, self._keypair
            )
            
            if "result" in transaction_signature:
                tx_id = transaction_signature["result"]
                return ToolResult.success(
                    tool_name=self.name,
                    result={
                        "transaction_signature": tx_id,
                        "from_address": str(self._keypair.public_key),
                        "to_address": recipient_address,
                        "amount_sol": amount,
                        "status": "submitted"
                    }
                )
            else:
                return ToolResult(
                    tool_name=self.name,
                    status="error",
                    error=f"Failed to submit transaction: {transaction_signature.get('error', 'Unknown error')}"
                )
        except ImportError:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Solana package not installed. Please install required packages."
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Error transferring SOL: {str(e)}"
            )
    
    def _get_token_balance(self, wallet_address: str, token_address: str) -> ToolResult:
        """Get SPL token balance for a wallet address"""
        if not wallet_address:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Wallet address is required"
            )
        
        if not token_address:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Token address is required"
            )
        
        try:
            from spl.token.client import Token
            from solana.publickey import PublicKey
            
            # Create token client
            token_client = Token(
                conn=self._client,
                pubkey=PublicKey(token_address),
                program_id=PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
                payer=None
            )
            
            # Get token account
            token_accounts = token_client.get_accounts(PublicKey(wallet_address))
            
            if not token_accounts.value:
                return ToolResult.success(
                    tool_name=self.name,
                    result={
                        "wallet_address": wallet_address,
                        "token_address": token_address,
                        "balance": 0,
                        "message": "No token account found for this token"
                    }
                )
            
            # Get token account info for the first token account
            account_info = token_accounts.value[0]
            token_amount = account_info.data.parsed['info']['tokenAmount']
            
            return ToolResult.success(
                tool_name=self.name,
                result={
                    "wallet_address": wallet_address,
                    "token_address": token_address,
                    "balance": float(token_amount['uiAmount']),
                    "decimals": token_amount['decimals']
                }
            )
        except ImportError:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="SPL token package not installed. Please install with 'pip install spl'"
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Error getting token balance: {str(e)}"
            )
    
    def _get_transaction(self, transaction_signature: str) -> ToolResult:
        """Get transaction details by signature"""
        if not transaction_signature:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Transaction signature is required"
            )
        
        try:
            response = self._client.get_transaction(transaction_signature)
            
            if "result" in response and response["result"]:
                return ToolResult.success(
                    tool_name=self.name,
                    result={
                        "transaction_signature": transaction_signature,
                        "transaction_details": response["result"]
                    }
                )
            else:
                return ToolResult(
                    tool_name=self.name,
                    status="error",
                    error=f"Transaction not found: {transaction_signature}"
                )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Error retrieving transaction: {str(e)}"
            )
    
    def _get_account_info(self, wallet_address: str) -> ToolResult:
        """Get account information for a wallet address"""
        if not wallet_address:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Wallet address is required"
            )
        
        try:
            response = self._client.get_account_info(wallet_address, encoding="jsonParsed")
            
            if "result" in response and response["result"] and "value" in response["result"]:
                return ToolResult.success(
                    tool_name=self.name,
                    result={
                        "wallet_address": wallet_address,
                        "account_info": response["result"]["value"]
                    }
                )
            else:
                return ToolResult.success(
                    tool_name=self.name,
                    result={
                        "wallet_address": wallet_address,
                        "account_info": None,
                        "message": "Account not found or empty"
                    }
                )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Error retrieving account info: {str(e)}"
            )
    
    def _create_token(self, token_name: str, token_symbol: str, token_decimals: int = 9, token_supply: float = 0) -> ToolResult:
        """Create a new SPL token"""
        if not self._keypair:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Private key not loaded. Please load a wallet first."
            )
        
        if not token_name or not token_symbol:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Token name and symbol are required"
            )
        
        try:
            from spl.token.instructions import create_mint
            from solana.system_program import CreateAccountParams, create_account
            from solana.transaction import Transaction
            from solana.publickey import PublicKey
            import random
            
            # Create a new keypair for the token mint
            from solana.keypair import Keypair
            mint_keypair = Keypair()
            
            # Calculate minimum balance for rent exemption
            resp = self._client.get_minimum_balance_for_rent_exemption(82)
            lamports = resp["result"]
            
            # Create system account for token mint
            create_account_ix = create_account(
                CreateAccountParams(
                    from_pubkey=self._keypair.public_key,
                    new_account_pubkey=mint_keypair.public_key,
                    lamports=lamports,
                    space=82,
                    program_id=PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
                )
            )
            
            # Create mint instruction
            create_mint_ix = create_mint(
                program_id=PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
                mint=mint_keypair.public_key,
                mint_authority=self._keypair.public_key,
                freeze_authority=self._keypair.public_key,
                decimals=token_decimals
            )
            
            # Create transaction with both instructions
            transaction = Transaction().add(create_account_ix).add(create_mint_ix)
            
            # Sign and send transaction
            transaction_signature = self._client.send_transaction(
                transaction, self._keypair, mint_keypair
            )
            
            if "result" in transaction_signature:
                tx_id = transaction_signature["result"]
                
                # If initial supply is specified, mint tokens
                if token_supply > 0:
                    self._mint_token(
                        token_address=str(mint_keypair.public_key),
                        recipient_address=str(self._keypair.public_key),
                        amount=token_supply
                    )
                
                return ToolResult.success(
                    tool_name=self.name,
                    result={
                        "transaction_signature": tx_id,
                        "token_address": str(mint_keypair.public_key),
                        "token_name": token_name,
                        "token_symbol": token_symbol,
                        "token_decimals": token_decimals,
                        "token_supply": token_supply,
                        "status": "created"
                    }
                )
            else:
                return ToolResult(
                    tool_name=self.name,
                    status="error",
                    error=f"Failed to create token: {transaction_signature.get('error', 'Unknown error')}"
                )
        except ImportError:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="SPL token package not installed. Please install required packages."
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Error creating token: {str(e)}"
            )
    
    def _mint_token(self, token_address: str, recipient_address: str, amount: float) -> ToolResult:
        """Mint tokens to a recipient address"""
        if not self._keypair:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Private key not loaded. Please load a wallet first."
            )
        
        if not token_address or not recipient_address:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Token address and recipient address are required"
            )
        
        if not amount or amount <= 0:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Valid amount is required (must be greater than 0)"
            )
        
        try:
            from spl.token.client import Token
            from spl.token.instructions import mint_to, MintToParams
            from solana.publickey import PublicKey
            from solana.transaction import Transaction
            
            # Get token info to determine decimals
            token_info = self._get_token_supply(token_address)
            if token_info.status == "error":
                return token_info
            
            token_decimals = token_info.result.get("decimals", 9)
            
            # Convert amount to token units
            token_amount = int(amount * (10 ** token_decimals))
            
            # Create token client
            token_client = Token(
                conn=self._client,
                pubkey=PublicKey(token_address),
                program_id=PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
                payer=self._keypair
            )
            
            # Get or create associated token account for recipient
            recipient_token_account = token_client.get_or_create_associated_token_account(
                owner=PublicKey(recipient_address)
            )
            
            # Create mint instruction
            mint_ix = mint_to(
                MintToParams(
                    program_id=PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
                    mint=PublicKey(token_address),
                    dest=recipient_token_account.value.address,
                    mint_authority=self._keypair.public_key,
                    amount=token_amount,
                    signers=[self._keypair.public_key]
                )
            )
            
            # Create transaction
            transaction = Transaction().add(mint_ix)
            
            # Sign and send transaction
            transaction_signature = self._client.send_transaction(
                transaction, self._keypair
            )
            
            if "result" in transaction_signature:
                tx_id = transaction_signature["result"]
                return ToolResult.success(
                    tool_name=self.name,
                    result={
                        "transaction_signature": tx_id,
                        "token_address": token_address,
                        "recipient_address": recipient_address,
                        "amount": amount,
                        "status": "minted"
                    }
                )
            else:
                return ToolResult(
                    tool_name=self.name,
                    status="error",
                    error=f"Failed to mint tokens: {transaction_signature.get('error', 'Unknown error')}"
                )
        except ImportError:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="SPL token package not installed. Please install required packages."
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Error minting tokens: {str(e)}"
            )
    
    def _get_token_supply(self, token_address: str) -> ToolResult:
        """Get token supply and info"""
        if not token_address:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Token address is required"
            )
        
        try:
            from spl.token.client import Token
            from solana.publickey import PublicKey
            
            # Create token client
            token_client = Token(
                conn=self._client,
                pubkey=PublicKey(token_address),
                program_id=PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
                payer=None
            )
            
            # Get token info
            resp = token_client.get_mint_info()
            
            if resp.value:
                mint_info = resp.value
                
                # Calculate total supply based on decimals
                supply = mint_info.supply
                decimals = mint_info.decimals
                total_supply = supply / (10 ** decimals)
                
                return ToolResult.success(
                    tool_name=self.name,
                    result={
                        "token_address": token_address,
                        "total_supply": total_supply,
                        "decimals": decimals,
                        "mint_authority": str(mint_info.mint_authority) if mint_info.mint_authority else None,
                        "freeze_authority": str(mint_info.freeze_authority) if mint_info.freeze_authority else None,
                        "is_initialized": mint_info.is_initialized
                    }
                )
            else:
                return ToolResult(
                    tool_name=self.name,
                    status="error",
                    error=f"Token not found: {token_address}"
                )
        except ImportError:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="SPL token package not installed. Please install required packages."
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error=f"Error getting token supply: {str(e)}"
            )
    
    def _swap_tokens(self, from_token: str, to_token: str, amount: float, slippage: float = 0.5) -> ToolResult:
        """Swap tokens using Raydium"""
        if not self._keypair:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Private key not loaded. Please load a wallet first."
            )
        
        return ToolResult(
            tool_name=self.name,
            status="error",
            error="This feature is a placeholder. Full Raydium AMM integration requires off-chain preparation."
        )
    
    def _provide_liquidity(self, token_a: str, token_b: str, amount_a: float, amount_b: float) -> ToolResult:
        """Provide liquidity to a Raydium pool"""
        if not self._keypair:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Private key not loaded. Please load a wallet first."
            )
        
        return ToolResult(
            tool_name=self.name,
            status="error",
            error="This feature is a placeholder. Full Raydium liquidity provision requires off-chain preparation."
        )
    
    def _stake_sol(self, amount: float, validator: str) -> ToolResult:
        """Stake SOL with a validator"""
        if not self._keypair:
            return ToolResult(
                tool_name=self.name,
                status="error",
                error="Private key not loaded. Please load a wallet first."
            )
        
        return ToolResult(
            tool_name=self.name,
            status="error",