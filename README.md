# SOLANUS: An Upgraded Web3 Version of ANUS

<p align="center">
  <img src="assets/header_solanus.png" alt="Anus AI Logo" width="800"/>
</p>

<p align="center">
  <img src="assets/solano.png" alt="Anus AI Logo" width="150"/>
</p>

## Introduction

SOLANUS is an advanced, Web3-enhanced autonomous AI agent built upon ANUS (Autonomous Networked Utility System). ANUS went viral as the first ever self-replicating agent, initially created by Manus AI next-gen agent. Manus AI attracted widespread attention due to its unexpected ability to replicate and deploy an open-source version of itself, an unprecedented capability among AI systems.

The inception of SOLANUS emerged from integrating Web3 functionalities into ANUS, significantly augmenting its capabilities by leveraging blockchain technologies provided by the Solana network. The primary purpose of SOLANUS is to enhance decentralized autonomous operations, bridging traditional AI functionality with on-chain blockchain processes, including asset management, decentralized interactions, and automated smart contract execution.

## Web3 Integration (New!)
SOLANUS has been significantly upgraded with cutting-edge Web3 capabilities:
- **Decentralized on-chain integration**: Direct interaction with the Solana blockchain.
- **Smart Contracts Automation**: Autonomous management and execution of blockchain-based tasks.
- **Digital Asset Handling**: Automated decentralized management and validation of tokens, NFTs, and digital assets.
- **Asset control and transaction management**
- **Data validation and integrity on-chain**

## Key Features
### What can SOLANUS do?

SOLANUS performs an extensive array of autonomous tasks, including:
- Information gathering, fact-checking, and documentation.
- Data processing, analysis, and visualization.
- Writing multi-chapter articles and in-depth research reports.
- Creating websites, applications, and digital tools.
- Developing and managing digital assets on blockchain.
- Building decentralized applications and smart contracts.
- Utilizing blockchain for automated, trustless interactions and management of digital assets.

### Web3 Functionalities:
- **Solana Blockchain Integration**: Enables SOLANUS to interact seamlessly with Solana's blockchain, manage assets, and automate on-chain transactions.
 - Asset management (tokens, NFTs, crypto assets)
 - Automated smart contract interactions
- **NFT & Digital Asset Management**: Creation, validation, trading, and custody management.
- **SocialFi & Decentralized Community Engagement**: Automating decentralized community interactions, providing user-friendly interfaces for blockchain communities, and facilitating decentralized applications.
- **GameFi & Game Mechanics**: Enables the implementation of play-to-earn mechanics, managing gaming assets, rewards, and blockchain-based games.

## Technical Capabilities
SOLANUS AI's autonomous capabilities include:

- Communication with users through message interfaces.
- Linux sandbox environment with internet access.
- Execution and management of shell scripts, text editing, browsing tasks, and code execution.
- Autonomous code writing and execution across multiple programming languages.
- Automated software package management and dependency installations.
- Deployment of publicly accessible websites, tools, and applications.
- Capability to temporarily hand over browser control for sensitive operations.
- Step-by-step task execution leveraging multiple integrated tools.

SOLANUS continues to evolve autonomously, pushing boundaries in decentralized artificial intelligence and revolutionizing the interaction between blockchain technology and advanced AI solutions.

## 🚀 Quick Start

```bash
# Install SolAnus
pip install solanus-ai

# Run with a basic task
solanus run "Find the latest news about artificial intelligence"

# Run a Web3 task
solanus run "Check the floor price for Degen Ape Academy NFT collection"
```

## 📋 Usage Examples

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

### Multi-Agent Collaboration

```python
from solanus import Society, Agent

# Create specialized agents for Web3 tasks
researcher = Agent(role="researcher", tools=["search", "browser"])
blockchain_expert = Agent(role="blockchain_expert", tools=["solana", "nft_analysis"])
developer = Agent(role="developer", tools=["code", "solana"])

# Create a society of agents
society = Society(agents=[researcher, blockchain_expert, developer])

# Execute complex Web3 task with collaboration
response = society.run(
    "Research the top 5 Solana NFT projects, analyze their floor prices, " 
    "and develop a simple dashboard to monitor them"
)
```

### NFT Creation and Analysis

```python
from solanus import Agent
from solanus.web3anustools import NFTCreationTool

# Create NFT-focused agent
agent = Agent(tools=["nft_creation", "nft_analysis"])

# Create and mint an NFT
nft_response = agent.run("""
Create an NFT with the following attributes:
Name: 'SOLANUS #1'
Description: 'First official SOLANUS AI generated NFT'
Attributes: [
    {"trait_type": "Background", "value": "Gradient Blue"},
    {"trait_type": "Character", "value": "Robot"},
    {"trait_type": "Accessory", "value": "Data Glasses"}
]
""")

# Analyze rarity and market value
analysis_response = agent.run(f"Analyze the rarity and estimated value of the NFT {nft_response['nft_address']}")
```

### Token-Gated Community Management

```python
from solanus import Agent
from solanus.web3anustools import TokenGatedCommunityTool

# Create community management agent
agent = Agent(tools=["token_gated_community"])

# Create a token-gated community
community_response = agent.run("""
Create a community called 'SOLANUS Innovators' that requires:
- At least 10 SOLANUS tokens OR
- Ownership of at least 1 SOLANUS NFT
""")

# Verify wallet access
verification_response = agent.run(f"""
Check if wallet GSAhLGBtiKZsxZVrjZLrYZSQHwbgjVrNgKWTq19TYJ8h
has access to the community {community_response['community_id']}
""")
```

### Advanced DeFi Integration

```python
from solanus import Agent
from solanus.web3anustools import DeFiTool, SolanaTool

# Create DeFi-focused agent
agent = Agent(tools=["defi", "solana"])

# Get optimal yield farming strategy
strategy_response = agent.run("""
Find the best yield farming strategy for 1000 USDC and 2 SOL
with maximum 14-day lockup period and moderate risk tolerance
""")

# Execute swap on Raydium
swap_response = agent.run("""
Swap 0.5 SOL to USDC on Raydium with 0.5% slippage
""")
```

### Command-Line Interface Examples

```bash
# Get real-time token pricing
solanus run "What is the current price of SOL, BONK, and JUP tokens?"

# Monitor wallet activity
solanus run --wallet=GSAhLGBtiKZsxZVrjZLrYZSQHwbgjVrNgKWTq19TYJ8h "Track transactions for this wallet"

# Analyze NFT collection
solanus run "What's the 30-day trading volume for DeGods collection?"

# Create smart contract
solanus run "Create a simple SPL token with 1 million supply, 6 decimals, and name 'SOLANUS Token'"
```

## Configuration

Create a `.solanus/config.yaml` file with your Web3 settings:

```yaml
web3:
  default_network: solana
  rpc_urls:
    solana: https://api.mainnet-beta.solana.com
    ethereum: https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY
  wallet:
    keypair_path: ~/.solanus/keypairs/solana_wallet.json
  
  # API keys for various services
  api_keys:
    nft_marketplace: YOUR_API_KEY
    game_platforms:
      axie_infinity: YOUR_AXIE_API_KEY
      star_atlas: YOUR_STAR_ATLAS_API_KEY
```

## Advanced Web3 Features

### Solana Program Deployment

```python
from solanus import Agent
from solanus.web3anustools import SolanaProgramTool

# Create agent with program deployment capabilities
agent = Agent(tools=["solana_program"])

# Deploy a simple Solana program
response = agent.run("""
Develop and deploy a simple Solana program that:
1. Stores a message on-chain
2. Allows the message owner to update it
3. Makes the message publicly readable
""")
```

### Cross-Chain Bridging

```python
from solanus import Agent
from solanus.web3anustools import CrossChainTool

# Create agent with cross-chain capabilities
agent = Agent(tools=["cross_chain", "solana", "ethereum"])

# Bridge assets from Ethereum to Solana
response = agent.run("""
Bridge 0.1 ETH from my Ethereum wallet 0x1234... 
to my Solana wallet GSAhLGB... using Wormhole
""")
```

## 👥 Contributing

We welcome contributions from the community! SOLANUS is designed to be community-driven, and your input helps make it better for everyone.

### Ways to Contribute

- **Code Contributions**: Implement new features, fix bugs, or improve performance
- **Documentation**: Improve or expand documentation, add examples, fix typos
- **Bug Reports**: Report bugs or suggest improvements
- **Feature Requests**: Suggest new features or enhancements
- **Community Support**: Help answer questions and support other users

### Getting Started with Contributing

1. **Fork the Repository**

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/your-username/SOLANUS.git
cd anus
```

2. **Set Up Development Environment**

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

3. **Create a Branch**

```bash
# Create a branch for your contribution
git checkout -b feature/your-feature-name
```

4. **Make Your Changes**

- Follow the code style guidelines
- Add tests for new functionality
- Update documentation as needed

5. **Run Tests**

```bash
# Run the test suite
pytest

# Run linting
flake8
mypy solanus
```

6. **Submit a Pull Request**

- Push your changes to your fork
- Submit a pull request from your branch to our main branch
- Provide a clear description of the changes and any related issues

### Code Style Guidelines

- Follow [PEP 8](https://pep8.org/) for Python code style
- Use type hints for all function parameters and return values
- Write docstrings for all functions, classes, and modules
- Keep functions focused and small (under 50 lines when possible)
- Use meaningful variable and function names

### Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

Types include:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code changes that neither fix bugs nor add features
- `test`: Adding or modifying tests
- `chore`: Changes to the build process or auxiliary tools

### Pull Request Process

1. Update the README.md or documentation with details of changes if appropriate
2. Update the CHANGELOG.md with details of changes
3. The PR should work for Python 3.11 and above
4. PRs require approval from at least one maintainer
5. Once approved, a maintainer will merge your PR

### Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.


## SOLANUS Community
Join our community to get help, share ideas, and contribute to the project:

- Twitter: https://x.com/solanus_ai
- Telegram: https://t.me/solanus_ai

## License

SOLANUS is released under the [MIT License](LICENSE).
