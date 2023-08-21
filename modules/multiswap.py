import random

from loguru import logger
from web3 import Web3
from config import SCROLL_TOKENS
from modules import Account, Uniswap
from utils.sleeping import sleep


class Multiswap(Account):
    def __init__(self, private_key: str, account_id: int) -> None:
        super().__init__(private_key=private_key, chain="scroll", account_id=account_id)

    def swap(
            self,
            sleep_from: int,
            sleep_to: int,
            min_swap: int,
            max_swap: int,
            slippage: int,
            all_amount: bool
    ):
        logger.info(f"{self.account_id}) [{self.address}] Start MultiSwap")

        quantity_swap = random.randint(min_swap, max_swap)

        for _ in range(0, quantity_swap):
            balance_eth = self.w3.eth.get_balance(self.address)
            balance_usdc = self.get_balance(SCROLL_TOKENS["GHO"])

            if balance_usdc["balance_wei"] > 0:
                all_amount = True if balance_usdc["balance"] <= 1 else all_amount
                decimal = balance_usdc["decimal"]
                min_amount = int(balance_usdc["balance"] * 0.1)
                max_amount = balance_usdc["balance"]
                from_token = "GHO"
                to_token = "ETH"
            else:
                all_amount = all_amount
                decimal = 18
                min_amount = float(Web3.from_wei(int(balance_eth * 0.1), "ether"))
                max_amount = float(Web3.from_wei(int(balance_eth * 0.9), "ether"))
                from_token = "ETH"
                to_token = "GHO"

            uniswap = Uniswap(self.private_key, self.account_id)
            uniswap.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount)

            if _ + 1 != quantity_swap:
                sleep(sleep_from, sleep_to)
