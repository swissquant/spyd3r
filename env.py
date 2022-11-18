import os
from dotenv import load_dotenv


# Loading the .env
load_dotenv()

# Wallet
ETH_ADDRESS = os.environ.get("ETH_ADDRESS", "")
ETH_PRIVATE_KEY = os.environ.get("ETH_PRIVATE_KEY", "")

# Nodes
WEB3_NODE = os.environ.get("WEB3_NODE", "")
