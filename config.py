import json
from pathlib import Path

with open('data/rpc.json') as file:
    RPC = json.load(file)

with open('data/abi/erc20_abi.json') as file:
    ERC20_ABI = json.load(file)

with open("accounts.txt", "r") as file:
    ACCOUNTS = [row.strip() for row in file]

with open('data/abi/scroll/bridge_ethereum.json') as file:
    BRIDGE_ETHEREUM_ABI = json.load(file)

with open('data/abi/scroll/bridge_scroll.json') as file:
    BRIDGE_SCROLL_ABI = json.load(file)

with open("data/abi/scroll/router.json", "r") as file:
    ROUTER_ABI = json.load(file)

with open("data/abi/scroll/quoter.json", "r") as file:
    QUOTER_ABI = json.load(file)

BRIDGE_CONTRACTS = {
    "ethereum": "0x13FBE0D0e5552b8c9c4AE9e2435F38f37355998a",
    "scroll": "0x9aD3c5617eCAa556d6E166787A97081907171230"
}

SCROLL_TOKENS = {
    "ETH": "0x5300000000000000000000000000000000000004",
    "GHO": "0xD9692f1748aFEe00FACE2da35242417dd05a8615",
}

UNISWAP_CONTRACTS = {
    "router": "0x17AFD0263D6909Ba1F9a8EAC697f76532365Fb95",
    "quoter": "0xd5dd33650Ef1DC6D23069aEDC8EAE87b0D3619B2"
}
