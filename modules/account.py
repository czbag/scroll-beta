import time
import random

from loguru import logger
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account as EthereumAccount
from web3.exceptions import TransactionNotFound

from config import RPC, ERC20_ABI, SCROLL_TOKENS


class Account:
    def __init__(self, private_key: str, chain: str, account_id: int) -> None:
        self.account_id = account_id
        self.private_key = private_key
        self.chain = chain
        self.explorer = RPC[chain]["explorer"]
        self.token = RPC[chain]["token"]

        self.w3 = Web3(Web3.HTTPProvider(random.choice(RPC[chain]["rpc"])))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.account = EthereumAccount.from_key(private_key)
        self.address = self.account.address

    def get_contract(self, contract_address: str, abi=None):
        contract_address = Web3.to_checksum_address(contract_address)

        if abi is None:
            abi = ERC20_ABI

        contract = self.w3.eth.contract(address=contract_address, abi=abi)

        return contract

    def get_balance(self, contract_address: str) -> dict:
        contract_address = Web3.to_checksum_address(contract_address)
        contract = self.get_contract(contract_address)

        symbol = contract.functions.symbol().call()
        decimal = contract.functions.decimals().call()
        balance_wei = contract.functions.balanceOf(self.address).call()

        balance = balance_wei / 10 ** decimal

        return {"balance_wei": balance_wei, "balance": balance, "symbol": symbol, "decimal": decimal}

    def get_amount(self, from_token: str, min_amount: float, max_amount: float, decimal: int, all_amount: bool):
        random_amount = round(random.uniform(min_amount, max_amount), decimal)

        if from_token == "ETH":
            balance = self.w3.eth.get_balance(self.address)
            amount_wei = int(balance * 0.9) if all_amount else Web3.to_wei(random_amount, "ether")
            amount = Web3.from_wei(int(balance * 0.9), "ether") if all_amount else random_amount
        else:
            balance = self.get_balance(SCROLL_TOKENS[from_token])
            amount_wei = balance["balance_wei"] if all_amount else int(random_amount * 10 ** balance["decimal"])
            amount = balance["balance"] if all_amount else random_amount
            balance = balance["balance_wei"]

        return amount_wei, amount, balance

    def check_allowance(self, token_address: str, contract_address: str) -> float:
        token_address = Web3.to_checksum_address(token_address)
        contract_address = Web3.to_checksum_address(contract_address)

        contract = self.w3.eth.contract(address=token_address, abi=ERC20_ABI)
        amount_approved = contract.functions.allowance(self.address, contract_address).call()

        return amount_approved

    def approve(self, amount: float, token_address: str, contract_address: str):
        token_address = Web3.to_checksum_address(token_address)
        contract_address = Web3.to_checksum_address(contract_address)

        contract = self.w3.eth.contract(address=token_address, abi=ERC20_ABI)

        allowance_amount = self.check_allowance(token_address, contract_address)

        if amount > allowance_amount:
            logger.success(f"{self.account_id}) [{self.address}] approve is successfully!")

            tx = {
                "chainId": self.w3.eth.chain_id,
                "from": self.address,
                "nonce": self.w3.eth.get_transaction_count(self.address),
                "gasPrice": self.w3.eth.gas_price,
            }

            transaction = contract.functions.approve(
                contract_address,
                100000000000000000000000000000000000000000000000000000000000000000000000000000
            ).build_transaction(tx)

            signed_txn = self.sign(transaction)

            txn_hash = self.send_raw_transaction(signed_txn)

            self.wait_until_tx_finished(txn_hash.hex())

    def wait_until_tx_finished(self, hash: str, max_wait_time=180):
        start_time = time.time()
        while True:
            try:
                receipts = self.w3.eth.get_transaction_receipt(hash)
                status = receipts.get("status")
                if status == 1:
                    logger.success(f"{self.account_id}) [{self.address}] {self.explorer}{hash} successfully!")
                    return True
                elif status is None:
                    time.sleep(0.3)
                elif status != 1:
                    logger.error(f"{self.account_id}) [{self.address}] {self.explorer}{hash} transaction failed!")
                    return False
            except TransactionNotFound:
                if time.time() - start_time > max_wait_time:
                    print(f'FAILED TX: {hash}')
                    return False
                time.sleep(1)

    def sign(self, transaction):
        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)

        return signed_txn

    def send_raw_transaction(self, signed_txn):
        txn_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return txn_hash
