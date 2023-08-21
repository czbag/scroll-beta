from web3 import Web3
from loguru import logger

from config import BRIDGE_CONTRACTS, BRIDGE_ETHEREUM_ABI, BRIDGE_SCROLL_ABI
from .account import Account


class Scroll(Account):
    def __init__(self, private_key: str, chain: str, account_id: int) -> None:
        super().__init__(private_key=private_key, chain=chain, account_id=account_id)

    def get_tx_data(self, value: int):
        tx = {
            "chainId": self.w3.eth.chain_id,
            "nonce": self.w3.eth.get_transaction_count(self.address),
            "from": self.address,
            "value": value
        }
        return tx

    def deposit(self, min_amount: float, max_amount: float, decimal: int, all_amount: bool):
        amount_wei, amount, balance = self.get_amount("ETH", min_amount, max_amount, decimal, all_amount)

        logger.info(f"{self.account_id}) [{self.address}] Bridge to Scroll | {amount} ETH")

        contract = self.get_contract(BRIDGE_CONTRACTS["ethereum"], BRIDGE_ETHEREUM_ABI)

        tx_data = self.get_tx_data(amount_wei + Web3.to_wei(0.01, "ether"))

        try:
            transaction = contract.functions.depositETH(amount_wei, 168000).build_transaction(tx_data)

            signed_txn = self.sign(transaction)

            txn_hash = self.send_raw_transaction(signed_txn)

            self.wait_until_tx_finished(txn_hash.hex())
            return txn_hash.hex()
        except Exception as e:
            logger.error(f"Deposit transaction on L1 network failed | error: {e}")

    def withdraw(self, min_amount: float, max_amount: float, decimal: int, all_amount: bool):
        amount_wei, amount, balance = self.get_amount("ETH", min_amount, max_amount, decimal, all_amount)

        logger.info(f"{self.account_id}) [{self.address}] Bridge to Ethereum Sepolia | {amount} ETH")

        contract = self.get_contract(BRIDGE_CONTRACTS["scroll"], BRIDGE_SCROLL_ABI)

        tx_data = self.get_tx_data(amount_wei)
        tx_data.update({"gasPrice": self.w3.eth.gas_price})


        try:
            transaction = contract.functions.withdrawETH(amount_wei, 0).build_transaction(tx_data)

            signed_txn = self.sign(transaction)

            txn_hash = self.send_raw_transaction(signed_txn)

            self.wait_until_tx_finished(txn_hash.hex())
            return txn_hash.hex()
        except Exception as e:
            logger.error(f"Withdraw transaction on L2 network failed | error: {e}")
