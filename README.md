# 🍑 SolAnus: A new web3 version of ANUS - Autonomous Networked Utility System

<p align="center">
  <img src="assets/anus_logo.png" alt="Anus AI Logo" width="150"/>
</p>

## 🌟 Introduction

**SolAnus** (Autonomous Networked Utility System) is a powerful, flexible, and accessible open-source AI agent framework designed to revolutionize task automation. It empowers users to create AI agents that can execute complex tasks through natural language, collaborate in multi-agent environments, and interact with various systems including cutting-edge Web3 technologies.

## 💡 Why SolAnus?

- **Open Source**: No barriers, just pure open-source goodness
- **Hybrid Architecture**: Combines single-agent simplicity with multi-agent power
- **Flexible Model Support**: Works with OpenAI models, open-source models, or your own
- **Comprehensive Tool Ecosystem**: Web automation, document processing, code execution, and more
- **Web3 Integration**: Interact with blockchains, NFTs, and decentralized protocols
- **Community-First Design**: Built for contributions and extensions

## ✨ Features & Capabilities

### 🧠 Advanced AI Agent Architecture
- Dynamic switching between single-agent and multi-agent modes
- Sophisticated task planning and resource allocation
- Short-term and long-term memory systems

### 🤝 Multi-Agent Collaboration
- Specialized agent roles with specific capabilities
- Collaborative decision-making through consensus
- Inter-agent communication protocols

### 🛠️ Tool Ecosystem
- Web automation and content extraction
- Document processing and code execution
- Web3 blockchain interactions

### 🌐 Web3 Integration (New!)
- **Solana Blockchain Integration**: Wallet management, token operations, transaction processing
- **NFT & Digital Assets**: Creation, analysis, trading, and collection management
- **SocialFi**: Token-gated communities and DAO governance tools
- **GameFi**: In-game asset management and play-to-earn mechanics

## 🚀 Quick Start

```bash
# Install SolAnus
pip install solanus-ai

# Run with a basic task
solanus run "Find the latest news about artificial intelligence"

# Run a Web3 task
solanus run "Check the floor price for Degen Ape Academy NFT collection"
```

## 📋 Examples

### Basic Usage

```python
from solanus import Agent

# Create a standard agent
agent = Agent()
response = agent.run("What is the capital of France?")
```

### Web3 Integration

```python
from solanus import Agent
from solanus.web3anustools import SolanaTool, NFTAnalysisTool

# Create an agent with Web3 capabilities
agent = Agent(tools=["solana", "nft_analysis"])

# Execute Solana transaction
response = agent.run("Transfer 0.5 SOL to Hx6LTcmUiC4EuWRG2nJQteHYpQvZWKhFTiweVjlxA3fG")

# Analyze NFT collection
response = agent.run("Compare floor prices of DeGods vs Okay Bears")
```

### GameFi Example

```python
from solanus import Agent

# Create a GameFi-focused agent
agent = Agent(tools=["game_asset_manager"])

# Check gaming inventory
response = agent.run("List all my assets in Star Atlas")
```

## 📚 Documentation

For detailed documentation, visit our [Documentation Site](https://anus-ai.github.io/docs).

## 👥 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

Anus is released under the [MIT License](LICENSE).
